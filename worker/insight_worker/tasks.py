import logging
import ocrmypdf
import fitz
import httpx
import json
from minio import Minio
from os import environ as env
from urllib.parse import urlparse
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from itertools import chain
from sqlalchemy import create_engine, select, text, inspect
from sqlalchemy.orm import Session
from .models import Files, Documents, Prompts, Sources, Pages
from .opensearch import opensearch_headers, opensearch_endpoint
from .rag import embed, complete


logging.basicConfig(level=logging.INFO)

engine = create_engine(env.get("POSTGRES_URI"))

minio = Minio(
    urlparse(env.get("STORAGE_ENDPOINT")).netloc,
    access_key=env.get("STORAGE_ACCESS_KEY"),
    secret_key=env.get("STORAGE_SECRET_KEY"),
    region="insight",
)


def orm_object_to_dict(obj):
    return {
        column.key: getattr(obj, column.key)
        for column in inspect(obj).mapper.column_attrs
    }


def ocrmypdf_process(input_file, output_file):
    ocrmypdf.ocr(
        input_file,
        output_file,
        language="nld",
        color_conversion_strategy="RGB",
        progress_bar=False,
        # https://github.com/ocrmypdf/OCRmyPDF/issues/1162
        continue_on_soft_render_error=True,
        # Only use one thread
        jobs=1,
        # Skip pages with text layer on it
        # TODO - Enable user to force OCR
        skip_text=True,
        # plugins=["insight_worker.plugin"],
    )


def analyze_file(id, channel):
    logging.info(f"Analyzing file {id}")

    with Session(engine) as session:
        stmt = select(Files).where(Files.id == id)
        file = session.scalars(stmt).one()

        file_path = Path(TemporaryDirectory().name) / "file.pdf"
        minio.fget_object(env.get("STORAGE_BUCKET"), file.path, file_path)

        with Pdf.open(file_path) as pdf:
            file.number_of_pages = len(pdf.pages)

        document = Documents(
            name=file.name,
            from_page=0,
            to_page=file.number_of_pages,
        )
        file.documents.append(document)
        file.status = None
        session.commit()

        channel.basic_publish(
            exchange="insight",
            routing_key="ingest_document",
            body=json.dumps({"id": str(document.id)}),
        )
        channel.basic_publish(
            exchange=f"user-{file.owner_id}",
            routing_key="analyze_file",
            body=json.dumps({"id": str(file.id)}),
        )


def ingest_document(id, channel):
    logging.info(f"Ingesting document {id}")

    temp_path = Path(TemporaryDirectory().name)
    file_path = temp_path / "file.pdf"
    split_path = temp_path / "split.pdf"
    ocr_path = temp_path / "ocr.pdf"

    with Session(engine) as session:
        stmt = select(Documents).join(Documents.file).where(Documents.id == id)
        document = session.scalars(stmt).one()

        minio.fget_object(env.get("STORAGE_BUCKET"), document.file.path, file_path)

        # Extract Document from file
        with Pdf.open(file_path) as file_pdf:
            before_range = range(0, document.from_page)
            after_range = range(document.to_page, document.file.number_of_pages)
            pages_to_delete = list(chain(before_range, after_range))
            # Reverse the range to remove last page first as the document shrinks
            # when removing pages, leading to IndexErrors otherwise
            for p in reversed(pages_to_delete):
                del file_pdf.pages[p]
            file_pdf.save(split_path)

        # OCR & optimize new PDF
        process = Process(target=ocrmypdf_process, args=(split_path, ocr_path))
        process.start()
        process.join()

        minio.fput_object(env.get("STORAGE_BUCKET"), document.path, ocr_path)

        # fitz is pyMuPDF used for extracting text layers
        document_pdf = fitz.open(ocr_path)

        # TODO - https://github.com/followthemoney/insight/issues/55

        # Get all contents, sorted by position on page
        contents = [page.get_text(sort=True) for page in document_pdf]
        # Get the embeddings for those contents
        embeddings = embed(contents)

        pages = [
            Pages(
                contents=contents,
                # Index pages in file instead of in document
                index=document.from_page + index,
                embedding=embedding,
                file_id=document.file.id,
            )
            for index, (contents, embedding) in enumerate(zip(contents, embeddings))
        ]
        session.add_all(pages)
        document.status = "indexing"
        session.commit()

        # Trigger indexing
        channel.basic_publish(
            exchange="insight",
            routing_key="index_document",
            body=json.dumps({"id": str(document.id)}),
        )
        channel.basic_publish(
            exchange=f"user-{document.file.owner_id}",
            routing_key="ingest_document",
            body=json.dumps({"id": str(document.id)}),
        )


def index_document(id, channel):
    logging.info(f"Indexing document {id}")

    with Session(engine) as session:
        stmt = select(Documents).join(Documents.file).where(Documents.id == id)
        document = session.scalars(stmt).one()

        # TODO - We can get these as part of the above documents query instead of 2
        stmt = (
            select(Pages.contents, Pages.index)
            .where(Pages.file_id == document.file.id)
            .where(Pages.index >= document.from_page)
            .where(Pages.index < document.to_page)
            .order_by(Pages.index.asc())
        )
        pages = session.execute(stmt).all()

        # Index files pages as document pages
        res = httpx.put(
            f"{opensearch_endpoint}/documents/_doc/{str(document.id)}",
            headers=opensearch_headers,
            json={
                "filename": document.name,
                "file_id": str(document.file.id),
                "pages": [
                    {
                        "document_id": str(document.id),
                        "index": index - document.from_page,
                        "contents": contents,
                    }
                    for (contents, index) in pages
                ],
            },
        )
        if res.status_code not in [200, 201]:
            raise Exception(res.text)

        document.status = None
        session.commit()

        # Notify user of our answer
        channel.basic_publish(
            exchange=f"user-{document.file.owner_id}",
            routing_key="index_document",
            body=json.dumps({"id": str(document.id)}),
        )


def delete_file(data, channel):
    logging.info(f"Deleting file {data['id']}")

    # Remove file from object storage
    minio.remove_object(env.get("STORAGE_BUCKET"), data["path"])


def delete_document(data, channel):
    logging.info(f"Deleting document {data['id']}")

    # Remove file from object storage
    minio.remove_object(env.get("STORAGE_BUCKET"), data["path"])

    # Remove indexed contents
    res = httpx.delete(
        f"{opensearch_endpoint}/documents/_doc/{data['id']}", headers=opensearch_headers
    )
    if res.status_code != 200:
        raise Exception(res.text)


def answer_prompt(id, channel):
    logging.info(f"Answering prompt {id}")

    # Get pages that have an embedding that is close to the query
    with Session(engine) as session:
        stmt = select(Prompts).where(Prompts.id == id)
        prompt = session.scalars(stmt).one()

        # Embed query
        embedding = next(embed([prompt.query]))

        stmt = (
            select(
                Pages.id,
                Pages.embedding.cosine_distance(embedding).label("distance"),
                Pages.contents,
            )
            .order_by(text("distance asc"))
            .limit(prompt.similarity_top_k)
        )

        pages = session.execute(stmt).all()

        # Create response by sending pages to chat completion
        response = complete(prompt.query, [contents for (_, _, contents) in pages])
        prompt.response = response

        for page_id, distance, _ in pages:
            source = Sources(
                page_id=page_id,
                similarity=(1 - distance) if distance is not None else 0,
            )
            prompt.sources.append(source)
        session.commit()

        channel.basic_publish(
            exchange=f"user-{prompt.owner_id}",
            routing_key="answer_prompt",
            body=json.dumps({"id": str(prompt.id)}),
        )
