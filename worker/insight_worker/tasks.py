import logging
import ocrmypdf
from os import environ as env
import fitz
import requests
from minio import Minio
from urllib.parse import urlparse
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from itertools import chain
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
from llama_index.schema import TextNode, NodeRelationship, RelatedNodeInfo
from .models import Files, Documents, Prompts, Sources
from .opensearch import opensearch_headers, opensearch_endpoint

vector_store = PGVectorStore.from_params(
    connection_string=env.get("POSTGRES_URI"),
    port=5432,
    schema_name="private",
    table_name="page",
    perform_setup=False,
    embed_dim=1536,
)

vector_store_index = VectorStoreIndex.from_vector_store(vector_store)

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


def analyze_file(data):
    logging.info(f"Analyzing file {data['id']}")

    file_path = Path(TemporaryDirectory().name) / "file.pdf"
    minio.fget_object(env.get("STORAGE_BUCKET"), data["path"], file_path)

    with Pdf.open(file_path) as pdf:
        pages = len(pdf.pages)

    with Session(engine) as session:
        stmt = select(Files).where(Files.id == data["id"])
        file = session.scalars(stmt).one()
        file.pages = pages
        file.status = "idle"

        document = Documents(
            name=data["name"],
            from_page=0,
            to_page=pages,
        )
        file.documents.append(document)
        session.commit()


def ingest_document(data):
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
        pages = len(file_pdf.pages)
        before_range = range(0, data["from_page"])
        after_range = range(data["to_page"], pages)
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
    # Sort sorts the text nodes by position on the page instead of order in the PDF structure
    page_contents = [page.get_text(sort=True) for page in document_pdf]

    # TODO - Remove embeddings of previous run
    pages = [
        {
            "file_id": data["file_id"],
            "index": data["from_page"] + index,
            "contents": contents,
        }
        for index, contents in enumerate(page_contents)
    ]

    nodes = [
        TextNode(
            text=page["contents"],
            id_=f"{page['file_id']}_{page['index']}",
            metadata={"file_id": page["file_id"], "index": page["index"]},
        )
        for page in pages
    ]
    for previous, current in zip(nodes[0:-1], nodes[1:]):
        previous.relationships[NodeRelationship.NEXT] = RelatedNodeInfo(
            node_id=current.node_id
        )
        current.relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(
            node_id=previous.node_id
        )
    vector_store_index.insert_nodes(nodes)

    body = {}
    body["filename"] = data["name"]
    body["pages"] = [
        {"document_id": data["id"], "index": index, "contents": contents}
        for index, contents in enumerate(page_contents)
    ]

    res = requests.put(
        f"{opensearch_endpoint}/documents/_doc/{data['id']}",
        headers=opensearch_headers,
        json=body,
    )
    if res.status_code != 201:
        raise Exception(res.text)

    with Session(engine) as session:
        stmt = select(Documents).where(Documents.id == data["id"])
        document = session.scalars(stmt).one()
        document.status = "idle"
        session.commit()


def delete_file(data):
    logging.info(f"Deleting file {data['id']}")

    # Remove file from object storage
    minio.remove_object(env.get("STORAGE_BUCKET"), data["path"])


def delete_document(data):
    logging.info(f"Deleting document {data['id']}")

    # Remove file from object storage
    minio.remove_object(env.get("STORAGE_BUCKET"), data["path"])

    # Remove indexed contents
    res = requests.delete(
        f"{env.get('API_ENDPOINT')}/index/_doc/{data['id']}", headers=headers
    )
    if res.status_code != 200:
        raise Exception(res.text)


def answer_prompt(data):
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
