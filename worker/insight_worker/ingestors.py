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
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import File
from .vectorstore import store_embeddings

engine = create_engine(env.get("POSTGRES_URI"))

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
        redo_ocr=True,
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

    session = Session(engine)
    file = File(name=name, from_page=0, to_page=to_page, pagestream_id=id)
    session.add(file)
    session.commit()

    logging.info(f"Saving pagestream {id} as file {file.id}")

    # OCR & optimize new PDF
    process = Process(target=ocrmypdf_process, args=(pagestream_path, file_path))
    process.start()
    process.join()
    minio.fput_object(env.get("STORAGE_BUCKET"), str(file.id), file_path)

    logging.info(f"Extracting metadata from file {file.id}")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/pdf",
    }
    res = requests.put(env.get("TIKA_URI"), data=open(file_path, "rb"), headers=headers)
    body = res.json()

    logging.info(f"Generating embeddings for file {file.id}")
    document = html.document_fromstring(body.pop("X-TIKA:content", None))
    pages = [
        {
            "pagestream_id": id,
            "index": file.from_page + index,
            "contents": page.text_content(),
        }
        for index, page in enumerate(document.find_class("page"))
    ]
    store_embeddings(pages)

    logging.info(f"Indexing file {file.id}")
    body["insight:filename"] = file.name
    body["insight:pages"] = [
        {"file_id": str(file.id), "index": index, "contents": page.text_content()}
        for index, page in enumerate(document.find_class("page"))
    ]

    res = requests.put(
        f"{env.get('ELASTICSEARCH_URI')}/insight/_doc/{file.id}", json=body
    )
    if res.status_code != 201:
        raise Exception(res.text)

    logging.info(f"Done processing of file {file.id}")
