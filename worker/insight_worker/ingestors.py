import logging
import ocrmypdf
import requests
from urllib.parse import urlparse
from os import environ as env
from minio import Minio
from xml.etree import ElementTree
from lxml import html
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from .vectorstore import store_embeddings
from .oauth import OAuth2Session


logging.basicConfig(level=logging.INFO)


def get_minio(token):
    res = requests.post(
        env.get("STORAGE_ENDPOINT"),
        data={
            "Action": "AssumeRoleWithWebIdentity",
            "Version": "2011-06-15",
            "DurationSeconds": "3600",
            "WebIdentityToken": token,
        },
    )
    tree = ElementTree.fromstring(res.content)
    ns = {"s3": "https://sts.amazonaws.com/doc/2011-06-15/"}
    credentials = tree.find("./s3:AssumeRoleWithWebIdentityResult/s3:Credentials", ns)

    return Minio(
        urlparse(env.get("STORAGE_ENDPOINT")).netloc,
        access_key=credentials.find("s3:AccessKeyId", ns).text,
        secret_key=credentials.find("s3:SecretAccessKey", ns).text,
        session_token=credentials.find("s3:SessionToken", ns).text,
        region="insight",
    )


def ocrmypdf_process(input_file, output_file):
    ocrmypdf.ocr(
        input_file,
        output_file,
        language="nld",
        force_ocr=True,
        color_conversion_strategy="RGB",
        # plugins=["insight_worker.plugin"],
    )


def ingest_file(id, owner_id, path, name, **kwargs):
    logging.info(f"Ingesting file {id}")

    temp_path = Path(TemporaryDirectory().name)
    file_path = temp_path / "file.pdf"
    document_path = temp_path / "document.pdf"

    session = OAuth2Session()
    minio = get_minio(session.token["access_token"])
    minio.fget_object(env.get("STORAGE_BUCKET"), path, file_path)

    with Pdf.open(file_path) as pdf:
        to_page = len(pdf.pages)

    res = session.post(
        f"{env.get('API_ENDPOINT')}/api/v1/documents",
        data={
            "owner_id": owner_id,
            "file_id": id,
            "name": name,
            "from_page": 0,
            "to_page": to_page,
        },
        headers={"Prefer": "return=representation"},
    )
    document = res.json()[0]

    logging.info(f"Saving file {id} as document {document['id']}")

    # OCR & optimize new PDF
    process = Process(target=ocrmypdf_process, args=(file_path, document_path))
    process.start()
    process.join()

    session = OAuth2Session()
    minio = get_minio(session.token["access_token"])
    minio.fput_object(env.get("STORAGE_BUCKET"), document["path"], document_path)

    logging.info(f"Extracting metadata from document {document['id']}")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/pdf",
    }
    res = requests.put(
        env.get("TIKA_URI"), data=open(document_path, "rb"), headers=headers
    )
    body = res.json()

    logging.info(f"Generating embeddings for document {document['id']}")
    html_doc = html.document_fromstring(body.pop("X-TIKA:content", None))
    pages = [
        {
            "file_id": id,
            "index": document["from_page"] + index,
            "contents": page.text_content(),
        }
        for index, page in enumerate(html_doc.find_class("page"))
    ]
    store_embeddings(pages)

    logging.info(f"Indexing document {document['id']}")
    body["insight:filename"] = document["name"]
    body["insight:pages"] = [
        {"document_id": document["id"], "index": index, "contents": page.text_content()}
        for index, page in enumerate(html_doc.find_class("page"))
    ]

    res = OAuth2Session().put(
        f"{env.get('API_ENDPOINT')}/api/v1/index/_doc/{document['id']}", json=body
    )
    if res.status_code != 201:
        raise Exception(res.text)

    res = session.patch(
        f"{env.get('API_ENDPOINT')}/api/v1/files?id=eq.{id}",
        data={"status": "idle"},
    )
    if res.status_code != 204:
        raise Exception(res.text)

    logging.info(f"Done processing of document {document['id']}")
