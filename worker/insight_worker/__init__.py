import os
import click
import logging
import asyncio
import json
import requests
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from urllib.parse import urlparse
from .models import File

logging.basicConfig(level=logging.INFO)

engine = create_engine(os.environ.get("POSTGRES_URI"))
conn = engine.connect()
conn.execute(text("listen page;"))
conn.commit()


def elasticsearch_url(path):
    url = urlparse(os.environ.get("ELASTICSEARCH_URI"))
    return url._replace(path=path).geturl()


def process_page(id, pagestream_id, index, contents):
    logging.info(f"Indexing page {id} at index {index} in pagestream {pagestream_id}")

    statement = (
        select(File)
        .where(File.pagestream_id == pagestream_id)
        .where(File.from_page <= index)
        .where(File.to_page > index)
    )
    with Session(engine) as session:
        file = session.scalar(statement)

    res = requests.put(
        elasticsearch_url(f"/insight/_doc/{id}"),
        json={
            "file_id": str(file.id),
            "file_name": file.name,
            "index": index - file.from_page,
            "contents": contents,
        },
    )

    if res.status_code != 201:
        raise Exception(res.text)


def reader():
    conn.connection.poll()
    for notification in conn.connection.notifies:
        object = json.loads(notification.payload)

        match notification.channel:
            case "page":
                process_page(**object)

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


@cli.command
def create_mapping():
    requests.put(
        elasticsearch_url(f"/insight"),
        json={
            "mappings": {
                "properties": {
                    "file_id": {"type": "keyword"},
                    "file_name": {"type": "keyword"},
                    "contents": {"type": "text"},
                    "index": {"type": "integer"},
                }
            }
        },
    )
