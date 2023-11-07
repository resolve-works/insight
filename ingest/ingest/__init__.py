import click
import psycopg2
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)

conn = psycopg2.connect(
    host=os.environ.get("PGHOST"),
    dbname=os.environ.get("PGDATABASE"),
    user=os.environ.get("PGUSER"),
    password=os.environ.get("PGPASSWORD"),
)

cursor = conn.cursor()
cursor.execute("LISTEN pagestreams;")
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
