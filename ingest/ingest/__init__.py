import click
import psycopg2
import asyncio
import os
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

engine = create_engine(
    "postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}".format(
        **os.environ
    )
)

conn = engine.connect()

cursor = conn.cursor()
cursor.execute("listen pagestreams;")
conn.commit()


def handle_notify():
    conn.poll()
    for notify in conn.notifies:
        logging.info(notify.payload)
    conn.notifies.clear()


@click.group()
def cli():
    pass


@cli.command()
def process_messages():
    logging.info("Processing messages")
    loop = asyncio.get_event_loop()
    loop.add_reader(conn, handle_notify)
    loop.run_forever()
