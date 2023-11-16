import click
import json
import asyncio
import os
import logging
import requests
from sqlalchemy import create_engine, text
from .ingestors import ingest_pagestream
from .vectorstore import answer_prompt

logging.basicConfig(level=logging.INFO)

engine = create_engine(os.environ.get("POSTGRES_URI"))
conn = engine.connect()
conn.execute(text("listen pagestream; listen file; listen prompt;"))
conn.commit()


# Make elastic treat pages as nested objects
def create_mapping():
    res = requests.put(
        f"{os.environ.get('ELASTICSEARCH_URI')}/insight",
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
    conn.connection.poll()
    for notification in conn.connection.notifies:
        object = json.loads(notification.payload)
        match notification.channel:
            case "pagestream":
                ingest_pagestream(**object)

    conn.connection.notifies.clear()


@click.group()
def cli():
    pass


@cli.command()
def process_messages():
    create_mapping()
    logging.info("Processing messages")
    loop = asyncio.get_event_loop()
    loop.add_reader(conn.connection, reader)
    loop.run_forever()
