import os
import logging
import ocrmypdf
import requests
from lxml import html
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import Pagestream, File
from .vectorstore import store_embeddings

engine = create_engine(os.environ.get("POSTGRES_URI"))


def ingest_pagestream(id, path, name, is_merged):
    logging.info(f"Ingesting pagestream {id}")

    with Pdf.open(path) as pdf:
        to_page = len(pdf.pages)

    with Session(engine) as session:
        file = File(name=name, from_page=0, to_page=to_page, pagestream_id=id)
        session.add(file)
        session.commit()


def ocrmypdf_process(input_file, output_file):
    ocrmypdf.ocr(
        input_file,
        output_file,
        language="nld",
        redo_ocr=True,
        # plugins=["insight_worker.plugin"],
    )


def extract_file(input_file, from_page, to_page, output_file):
    destination = Pdf.new()
    with Pdf.open(input_file) as pdf:
        for page in pdf.pages[from_page:to_page]:
            destination.pages.append(page)
        destination.copy_foreign(pdf.docinfo)
        destination.save(output_file)


def ingest_file(id, pagestream_id, from_page, to_page, name):
    with Session(engine) as session:
        pagestream = session.query(Pagestream).get(pagestream_id)

    files_path = Path(os.environ.get("INSIGHT_FILES_PATH"))
    if not files_path.exists():
        files_path.mkdir()

    if pagestream.is_merged:
        logging.info(f"Saving pages {from_page}:{to_page} as file {id}")
        # Extract file from pagestream
        source_file = Path(TemporaryDirectory()) / "file.pdf"
        extract_file(pagestream.path, from_page, to_page, source_file)
    else:
        logging.info(f"Saving pagestream {pagestream_id} as file {id}")
        source_file = pagestream.path

    # OCR & optimize new PDF
    output_file = files_path / f"{id}.pdf"
    process = Process(target=ocrmypdf_process, args=(source_file, output_file))
    process.start()
    process.join()

    logging.info(f"Extracting metadata from file {id}")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/pdf",
    }
    res = requests.put(
        os.environ.get("TIKA_URI"), data=open(output_file, "rb"), headers=headers
    )
    body = res.json()

    logging.info(f"Generating embeddings for file {id}")
    document = html.document_fromstring(body.pop("X-TIKA:content", None))
    # Pages relative to file (not pagestream containing file)
    pages = [
        {"file_id": id, "index": index, "contents": page.text_content()}
        for index, page in enumerate(document.find_class("page"))
    ]
    store_embeddings(pages)

    logging.info(f"Indexing file {id}")
    body["insight:filename"] = name
    body["insight:pages"] = pages

    res = requests.put(
        f"{os.environ.get('ELASTICSEARCH_URI')}/insight/_doc/{id}", json=body
    )
    if res.status_code != 201:
        raise Exception(res.text)

    logging.info(f"Done processing of file {id}")
