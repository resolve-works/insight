import os
import click
import logging
import asyncio
import json
import psycopg2
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

conn = psycopg2.connect(os.environ.get("POSTGRES_URI"))
cursor = conn.cursor()
cursor.execute("LISTEN page;")
conn.commit()


def elasticsearch_url(path):
    url = urlparse(os.environ.get("ELASTICSEARCH_URI"))
    return url._replace(path=path).geturl()


def process_page(id, pagestream_id):
    logging.info(f"{id}")


def reader():
    conn.poll()
    for notification in conn.notifies:
        object = json.loads(notification.payload)

        match notification.channel:
            case "page":
                process_page(**object)

    conn.notifies.clear()


@click.group()
def cli():
    pass


@cli.command()
def process_messages():
    logging.info("Processing messages")
    loop = asyncio.get_event_loop()
    loop.add_reader(conn, reader)
    loop.run_forever()
