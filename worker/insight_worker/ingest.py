import logging
import ocrmypdf
from os import environ as env
import fitz
import requests
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from itertools import chain
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from .vectorstore import store_embeddings
from .storage import minio
from .models import Files, Documents
from .opensearch import headers

logging.basicConfig(level=logging.INFO)

engine = create_engine(env.get("POSTGRES_URI"))


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
        for p in chain(range(0, data["from_page"]), range(data["to_page"], pages)):
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
    store_embeddings(pages)

    body = {}
    body["filename"] = data["name"]
    body["pages"] = [
        {"document_id": data["id"], "index": index, "contents": contents}
        for index, contents in enumerate(page_contents)
    ]

    res = requests.put(
        f"{env.get('API_ENDPOINT')}/index/_doc/{data['id']}",
        headers=headers,
        json=body,
    )
    if res.status_code != 201:
        raise Exception(res.text)

    with Session(engine) as session:
        stmt = select(Documents).where(Documents.id == data["id"])
        document = session.scalars(stmt).one()
        document.status = "idle"
        session.commit()


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
