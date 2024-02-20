import click
import os
import logging
from .ingest import analyze_file, ingest_document
from .delete import delete_document
from .oauth import OAuth2Session

logging.basicConfig(level=logging.INFO)


# Make elastic treat pages as nested objects
def create_mapping():
    logging.info("Creating index")

    res = OAuth2Session().put(
        f"{os.environ.get('API_ENDPOINT')}/index",
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


@click.group()
def cli():
    pass


@cli.command()
def process_messages():
    create_mapping()
    logging.info("Processing messages")
    # TODO - Attach to queue
