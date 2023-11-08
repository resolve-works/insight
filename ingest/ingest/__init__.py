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

engine = create_engine(os.environ.get("PG_DB_URI"))
conn = engine.connect()
conn.execute(text("listen pagestream; listen file;"))
conn.commit()


def process_pagestream(id, path, name):
    logging.info(f"Ingesting pagestream {id}")

    with Pdf.open(path) as pdf:
        count = len(pdf.pages)

    with Session(engine) as session:
        file = File(
            name=name,
            first_page=0,
            last_page=count - 1,
            pagestream_id=id,
        )

        session.add(file)
        session.commit()


def ocrmypdf_process(input_file, output_file):
    ocrmypdf.ocr(input_file, output_file, force_ocr=True, language="nld")


def process_file(id, pagestream_id, first_page, last_page, name):
    logging.info(f"Ingesting file {id}")

    with Session(engine) as session:
        pagestream = session.query(Pagestream).get(pagestream_id)

    with TemporaryDirectory() as directory:
        temp_file = Path(directory) / "file.pdf"

        # Split PDF from pagestream
        destination = Pdf.new()
        logging.info(f"Saving pages {first_page}:{last_page} - {name}")
        with Pdf.open(pagestream.path) as pdf:
            for page in pdf.pages[first_page:last_page]:
                destination.pages.append(page)
            destination.copy_foreign(pdf.docinfo)
            destination.save(temp_file)

        # OCR & optimize new PDF
        output_file = Path(os.environ.get("INGEST_FILES_PATH")) / f"{id}.pdf"
        ocrmypdf.ocr(temp_file, output_file, force_ocr=True)
        p = Process(target=ocrmypdf_process, args=(temp_file, output_file))
        p.start()
        p.join()


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
