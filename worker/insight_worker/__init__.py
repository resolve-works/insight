import click
import json
import asyncio
import os
import logging
import requests
import psycopg2
from .ingestors import ingest_pagestream

logging.basicConfig(level=logging.INFO)

conn = psycopg2.connect(os.environ.get("POSTGRES_URI"))
cursor = conn.cursor()
cursor.execute(f"LISTEN pagestream;")
conn.commit()


# Make elastic treat pages as nested objects
def create_mapping():
    res = requests.put(
        f"{os.environ.get('API_ENDPOINT')}/api/v1/index",
        json={"mappings": {"properties": {"insight:pages": {"type": "nested"}}}},
    )

    if res.status_code == 200:
        return
    elif (
        res.status_code == 400
        and res.json()["error"]["type"] == "resource_already_exists_exception"
    ):
        return
    else:
        raise Exception(res.text)


def reader():
    conn.poll()
    for notification in conn.notifies:
        object = json.loads(notification.payload)
        match notification.channel:
            case "pagestream":
                ingest_pagestream(**object)

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
