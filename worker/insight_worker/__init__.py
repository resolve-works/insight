import click
import asyncio
import os
import logging
import psycopg2
from .ingest import ingest_file, ingest_document
from .delete import delete_document
from .oauth import OAuth2Session

logging.basicConfig(level=logging.INFO)

conn = psycopg2.connect(os.environ.get("POSTGRES_URI"))
cursor = conn.cursor()
cursor.execute(f"LISTEN ingest_file; LISTEN ingest_document; LISTEN delete_document;")
conn.commit()


# Make elastic treat pages as nested objects
def create_mapping():
    logging.info("Creating index")

    res = OAuth2Session().put(
        f"{os.environ.get('API_ENDPOINT')}/api/v1/index",
        json={"mappings": {"properties": {"pages": {"type": "nested"}}}},
    )

    if res.status_code == 200:
        logging.info("Index created succesfully")
        return
    elif (
        res.status_code == 400
        and res.json()["error"]["type"] == "resource_already_exists_exception"
    ):
        logging.info("Index creation skipped, index already exists")
        return
    else:
        raise Exception(res.text)


def reader():
    conn.poll()
    for notification in conn.notifies:
        match notification.channel:
            case "ingest_file":
                ingest_file(notification.payload)
            case "ingest_document":
                ingest_document(notification.payload)
            case "delete_document":
                delete_document(notification.payload)

    conn.notifies.clear()


@click.group()
def cli():
    pass


@cli.command()
def process_messages():
    create_mapping()
    logging.info("Processing messages")
    loop = asyncio.get_event_loop()
    loop.add_reader(conn, reader)
    loop.run_forever()
