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


def ingest_pagestream(id, owner_id, path, name, **kwargs):
    logging.info(f"Ingesting pagestream {id}")

    temp_path = Path(TemporaryDirectory().name)
    pagestream_path = temp_path / "pagestream.pdf"
    file_path = temp_path / "file.pdf"

    session = OAuth2Session()
    minio = get_minio(session.token["access_token"])
    minio.fget_object(env.get("STORAGE_BUCKET"), path, pagestream_path)

    with Pdf.open(pagestream_path) as pdf:
        to_page = len(pdf.pages)

    res = session.post(
        f"{env.get('API_ENDPOINT')}/api/v1/file",
        data={
            "owner_id": owner_id,
            "pagestream_id": id,
            "name": name,
            "from_page": 0,
            "to_page": to_page,
        },
        headers={"Prefer": "return=representation"},
    )
    file = res.json()[0]

    logging.info(f"Saving pagestream {id} as file {file['id']}")

    # OCR & optimize new PDF
    process = Process(target=ocrmypdf_process, args=(pagestream_path, file_path))
    process.start()
    process.join()

    session = OAuth2Session()
    minio = get_minio(session.token["access_token"])
    minio.fput_object(env.get("STORAGE_BUCKET"), file["path"], file_path)

    logging.info(f"Extracting metadata from file {file['id']}")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/pdf",
    }
    res = requests.put(env.get("TIKA_URI"), data=open(file_path, "rb"), headers=headers)
    body = res.json()

    logging.info(f"Generating embeddings for file {file['id']}")
    document = html.document_fromstring(body.pop("X-TIKA:content", None))
    pages = [
        {
            "pagestream_id": id,
            "index": file["from_page"] + index,
            "contents": page.text_content(),
        }
        for index, page in enumerate(document.find_class("page"))
    ]
    store_embeddings(pages)

    logging.info(f"Indexing file {file['id']}")
    body["insight:filename"] = file["name"]
    body["insight:pages"] = [
        {"file_id": file["id"], "index": index, "contents": page.text_content()}
        for index, page in enumerate(document.find_class("page"))
    ]

    res = OAuth2Session().put(
        f"{env.get('API_ENDPOINT')}/api/v1/index/_doc/{file['id']}", json=body
    )
    if res.status_code != 201:
        raise Exception(res.text)

    res = session.patch(
        f"{env.get('API_ENDPOINT')}/api/v1/pagestream?id=eq.{id}",
        data={"status": "idle"},
    )
    if res.status_code != 204:
        raise Exception(res.text)

    logging.info(f"Done processing of file {file['id']}")
