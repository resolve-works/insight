import logging
import ocrmypdf
from os import environ as env
import fitz
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from itertools import chain
from .vectorstore import store_embeddings
from .storage import get_minio
from .oauth import OAuth2Session


logging.basicConfig(level=logging.INFO)


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


def ingest_file(id):
    session = OAuth2Session()
    res = session.patch(
        f"{env.get('API_ENDPOINT')}/api/v1/files?id=eq.{id}",
        data={"status": "analyzing"},
    )
    if res.status_code != 204:
        raise Exception(res.text)

    res = session.get(f"{env.get('API_ENDPOINT')}/api/v1/files?id=eq.{id}")
    file = res.json()[0]

    logging.info(f"Ingesting file {file['id']}")
    file_path = Path(TemporaryDirectory().name) / "file.pdf"

    minio = get_minio(session.token["access_token"])
    minio.fget_object(env.get("STORAGE_BUCKET"), file["path"], file_path)

    with Pdf.open(file_path) as pdf:
        pages = len(pdf.pages)

    res = session.patch(
        f"{env.get('API_ENDPOINT')}/api/v1/files?id=eq.{file['id']}",
        data={"pages": pages, "status": "idle"},
    )
    if res.status_code != 204:
        raise Exception(res.text)

    # We're assuming that file contains 1 document spanning all the pages in the file.
    res = session.post(
        f"{env.get('API_ENDPOINT')}/api/v1/documents",
        data={
            "owner_id": file["owner_id"],
            "file_id": file["id"],
            "name": file["name"],
            "from_page": 0,
            "to_page": pages,
        },
        headers={"Prefer": "return=representation"},
    )
    if res.status_code != 201:
        raise Exception(res.text)

    document = res.json()[0]
    logging.info(f"Created document {document['id']}")

    res = session.post(
        f"{env.get('API_ENDPOINT')}/api/v1/rpc/ingest_document",
        data={"id": document["id"]},
    )
    if res.status_code != 204:
        raise Exception(res.text)


def ingest_document(id):
    session = OAuth2Session()
    res = session.get(
        f"{env.get('API_ENDPOINT')}/api/v1/documents?select=id,name,path,from_page,to_page,file_id,files(path)&id=eq.{id}"
    )
    document = res.json()[0]

    res = session.patch(
        f"{env.get('API_ENDPOINT')}/api/v1/documents?id=eq.{document['id']}",
        data={"status": "ingesting"},
    )
    if res.status_code != 204:
        raise Exception(res.text)

    logging.info(
        f"Extracting pages {document['from_page']} to {document['to_page']} of file {document['file_id']} as document {document['id']}"
    )

    temp_path = Path(TemporaryDirectory().name)
    file_path = temp_path / "file.pdf"
    intermediate_path = temp_path / "intermediate.pdf"
    document_path = temp_path / "final.pdf"

    minio = get_minio(session.token["access_token"])
    minio.fget_object(env.get("STORAGE_BUCKET"), document["files"]["path"], file_path)

    # Extract Document from file
    with Pdf.open(file_path) as file_pdf:
        pages = len(file_pdf.pages)
        for p in chain(
            range(0, document["from_page"]), range(document["to_page"], pages)
        ):
            del file_pdf.pages[p]
        file_pdf.save(intermediate_path)

    # OCR & optimize new PDF
    process = Process(target=ocrmypdf_process, args=(intermediate_path, document_path))
    process.start()
    process.join()

    session = OAuth2Session()
    minio = get_minio(session.token["access_token"])
    minio.fput_object(env.get("STORAGE_BUCKET"), document["path"], document_path)

    logging.info(f"Generating embeddings for document {document['id']}")

    document_pdf = fitz.open(document_path)  # open a document
    page_contents = [page.get_text(sort=True) for page in document_pdf]

    pages = [
        {
            "file_id": document["file_id"],
            "index": document["from_page"] + index,
            "contents": contents,
        }
        for index, contents in enumerate(page_contents)
    ]
    store_embeddings(pages)

    body = {}
    logging.info(f"Indexing document {document['id']}")
    body["filename"] = document["name"]
    body["pages"] = [
        {"document_id": document["id"], "index": index, "contents": contents}
        for index, contents in enumerate(page_contents)
    ]

    res = OAuth2Session().put(
        f"{env.get('API_ENDPOINT')}/api/v1/index/_doc/{document['id']}", json=body
    )
    if res.status_code != 201:
        raise Exception(res.text)

    res = session.patch(
        f"{env.get('API_ENDPOINT')}/api/v1/documents?id=eq.{document['id']}",
        data={"status": "idle"},
    )
    if res.status_code != 204:
        raise Exception(res.text)

    logging.info(f"Done processing of document {id}")
