import click
import json
import asyncio
import os
import logging
import ocrmypdf
from multiprocessing import Process
from tempfile import TemporaryDirectory
from pathlib import Path
from pikepdf import Pdf
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from .models import Pagestream, File

logging.basicConfig(level=logging.INFO)

engine = create_engine(os.environ.get("POSTGRES_URI"))
conn = engine.connect()
conn.execute(text("listen pagestream; listen file;"))
conn.commit()


def process_pagestream(id, path, name):
    logging.info(f"Ingesting pagestream {id}")

    with Pdf.open(path) as pdf:
        to_page = len(pdf.pages)

    with Session(engine) as session:
        file = File(name=name, from_page=0, to_page=to_page, pagestream_id=id)
        session.add(file)
        session.commit()


def ocrmypdf_process(input_file, output_file, file_id):
    ocrmypdf.ocr(
        input_file,
        output_file,
        force_ocr=True,
        language="nld",
        plugins=["ingest.plugin"],
        file_id=file_id,
    )


def extract_file(input_file, from_page, to_page, output_file):
    destination = Pdf.new()
    with Pdf.open(input_file) as pdf:
        for page in pdf.pages[from_page:to_page]:
            destination.pages.append(page)
        destination.copy_foreign(pdf.docinfo)
        destination.save(output_file)


def process_file(id, pagestream_id, from_page, to_page, name):
    logging.info(f"Saving pages {from_page}:{to_page} as file {id}")

    with Session(engine) as session:
        pagestream = session.query(Pagestream).get(pagestream_id)

    with TemporaryDirectory() as directory:
        temp_file = Path(directory) / "file.pdf"

        # Extract file from pagestream
        extract_file(pagestream.path, from_page, to_page, temp_file)

        # OCR & optimize new PDF
        output_file = Path(os.environ.get("INGEST_FILES_PATH")) / f"{id}.pdf"
        process = Process(target=ocrmypdf_process, args=(temp_file, output_file, id))
        process.start()
        process.join()


def reader():
    conn.connection.poll()
    for notification in conn.connection.notifies:
        object = json.loads(notification.payload)

        match notification.channel:
            case "pagestream":
                process_pagestream(**object)
            case "file":
                process_file(**object)

    conn.connection.notifies.clear()


@click.group()
def cli():
    pass


@cli.command()
def process_messages():
    logging.info("Processing messages")
    loop = asyncio.get_event_loop()
    loop.add_reader(conn.connection, reader)
    loop.run_forever()
