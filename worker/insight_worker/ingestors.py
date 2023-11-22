import logging
import ocrmypdf
import requests
from os import environ as env
from minio import Minio
from lxml import html
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from .vectorstore import store_embeddings


logging.basicConfig(level=logging.INFO)

client = BackendApplicationClient(client_id=env.get("AUTH_CLIENT_ID"))
token = OAuth2Session(client=client).fetch_token(
    client_id=env.get("AUTH_CLIENT_ID"),
    token_url=env.get("AUTH_TOKEN_ENDPOINT"),
    client_secret=env.get("AUTH_CLIENT_SECRET"),
)


def save_token(new_token):
    global token
    logging.info("Storing token")
    logging.info(new_token.keys())
    token = new_token


session = OAuth2Session(
    client_id=env.get("AUTH_CLIENT_ID"),
    token=token,
    auto_refresh_url=env.get("AUTH_TOKEN_ENDPOINT"),
    auto_refresh_kwargs={
        "client_id": env.get("AUTH_CLIENT_ID"),
    },
    token_updater=save_token,
)

minio = Minio(
    env.get("STORAGE_ENDPOINT"),
    access_key=env.get("STORAGE_ACCESS_KEY"),
    secret_key=env.get("STORAGE_SECRET_KEY"),
    secure=env.get("STORAGE_SECURE").lower() == "true",
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


def ingest_pagestream(id, name, is_merged):
    logging.info(f"Ingesting pagestream {id}")

    temp_path = Path(TemporaryDirectory().name)
    pagestream_path = temp_path / "pagestream.pdf"
    file_path = temp_path / "file.pdf"

    minio.fget_object(env.get("STORAGE_BUCKET"), id, pagestream_path)

    with Pdf.open(pagestream_path) as pdf:
        to_page = len(pdf.pages)

    res = session.post(
        f"{env.get('API_ENDPOINT')}/api/v1/file",
        data={"pagestream_id": id, "name": name, "from_page": 0, "to_page": to_page},
        headers={"Prefer": "return=representation"},
    )
    file = res.json()[0]

    logging.info(f"Saving pagestream {id} as file {file['id']}")

    # OCR & optimize new PDF
    process = Process(target=ocrmypdf_process, args=(pagestream_path, file_path))
    process.start()
    process.join()
    minio.fput_object(env.get("STORAGE_BUCKET"), str(file["id"]), file_path)

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

    res = requests.put(
        f"{env.get('API_ENDPOINT')}/api/v1/index/_doc/{file['id']}", json=body
    )
    if res.status_code != 201:
        raise Exception(res.text)

    logging.info(f"Done processing of file {file['id']}")
