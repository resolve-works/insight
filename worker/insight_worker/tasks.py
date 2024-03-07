import logging
import ocrmypdf
import fitz
import httpx
from minio import Minio
from os import environ as env
from urllib.parse import urlparse
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from itertools import chain
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from .models import Files, Documents, Prompts, Sources, Pages
from .opensearch import opensearch_headers, opensearch_endpoint
from .rag import embed


logging.basicConfig(level=logging.INFO)

engine = create_engine(env.get("POSTGRES_URI"))

minio = Minio(
    urlparse(env.get("STORAGE_ENDPOINT")).netloc,
    access_key=env.get("STORAGE_ACCESS_KEY"),
    secret_key=env.get("STORAGE_SECRET_KEY"),
    region="insight",
)


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


def analyze_file(data, notify_user):
    logging.info(f"Analyzing file {data['id']}")

    file_path = Path(TemporaryDirectory().name) / "file.pdf"
    minio.fget_object(env.get("STORAGE_BUCKET"), data["path"], file_path)

    with Pdf.open(file_path) as pdf:
        number_of_pages = len(pdf.pages)

    with Session(engine) as session:
        stmt = select(Files).where(Files.id == data["id"])
        file = session.scalars(stmt).one()
        file.number_of_pages = number_of_pages
        file.status = "idle"

        document = Documents(
            name=data["name"],
            from_page=0,
            to_page=number_of_pages,
        )
        file.documents.append(document)
        session.commit()

    # Notify user of our answer
    notify_user(data["owner_id"], "analyze_file", data["id"])


def ingest_document(data, notify_user):
    logging.info(f"Ingesting document {data['id']}")

    temp_path = Path(TemporaryDirectory().name)
    file_path = temp_path / "file.pdf"
    intermediate_path = temp_path / "intermediate.pdf"
    document_path = temp_path / "final.pdf"

    with Session(engine) as session:
        stmt = select(Files).where(Files.id == data["file_id"])
        file = session.scalars(stmt).one()

    minio.fget_object(env.get("STORAGE_BUCKET"), file.path, file_path)

    # Extract Document from file
    with Pdf.open(file_path) as file_pdf:
        number_of_pages = len(file_pdf.pages)
        before_range = range(0, data["from_page"])
        after_range = range(data["to_page"], number_of_pages)
        pages_to_delete = list(chain(before_range, after_range))
        # Reverse the range to remove last page first as the document shrinks
        # when removing pages, leading to IndexErrors otherwise
        for p in reversed(pages_to_delete):
            del file_pdf.pages[p]
        file_pdf.save(intermediate_path)

    # OCR & optimize new PDF
    process = Process(target=ocrmypdf_process, args=(intermediate_path, document_path))
    process.start()
    process.join()

    minio.fput_object(env.get("STORAGE_BUCKET"), data["path"], document_path)

    # fitz is pyMuPDF used for extracting text layers
    document_pdf = fitz.open(document_path)
    # Get all contents, sorted by position on page
    contents = [page.get_text(sort=True) for page in document_pdf]
    # Get the embeddings for those contents
    embeddings = embed(contents)

    with Session(engine) as session:
        pages = [
            Pages(
                contents=contents,
                index=index,
                embedding=embedding,
                file_id=data["file_id"],
            )
            for index, (contents, embedding) in enumerate(zip(contents, embeddings))
        ]
        session.add_all(pages)
        session.commit()

    # body = {}
    # body["filename"] = data["name"]
    # body["pages"] = [
    # {"document_id": data["id"], "index": index, "contents": contents}
    # for index, contents in enumerate(page_contents)
    # ]

    # res = httpx.put(
    # f"{opensearch_endpoint}/documents/_doc/{data['id']}",
    # headers=opensearch_headers,
    # json=body,
    # )
    # if res.status_code != 201:
    # raise Exception(res.text)

    with Session(engine) as session:
        stmt = select(Documents).where(Documents.id == data["id"])
        document = session.scalars(stmt).one()
        document.status = "idle"
        session.commit()

    # Notify user of our answer
    notify_user(file.owner_id, "ingest_document", data["id"])


def delete_file(data, notify_user):
    logging.info(f"Deleting file {data['id']}")

    # Remove file from object storage
    minio.remove_object(env.get("STORAGE_BUCKET"), data["path"])


def delete_document(data, notify_user):
    logging.info(f"Deleting document {data['id']}")

    # Remove file from object storage
    minio.remove_object(env.get("STORAGE_BUCKET"), data["path"])

    # Remove indexed contents
    res = httpx.delete(
        f"{opensearch_endpoint}/documents/_doc/{data['id']}", headers=opensearch_headers
    )
    if res.status_code != 200:
        raise Exception(res.text)


def answer_prompt(data, notify_user):
    logging.info(f"Answering prompt {data['id']}")

    query_engine = vector_store_index.as_query_engine(
        similarity_top_k=data["similarity_top_k"]
    )
    response = query_engine.query(data["query"])

    with Session(engine) as session:
        stmt = select(Prompts).where(Prompts.id == data["id"])
        prompt = session.scalars(stmt).one()
        prompt.response = response.response

        for node in response.source_nodes:
            source = Sources(
                file_id=node.metadata["file_id"],
                index=node.metadata["index"],
                score=node.get_score(),
            )
            prompt.sources.append(source)
        session.commit()

    notify_user(data["owner_id"], "answer_prompt", data["id"])
