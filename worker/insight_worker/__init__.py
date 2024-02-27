import click
import logging
import json
import requests
from os import environ as env
from pika import ConnectionParameters, SelectConnection, PlainCredentials
from .tasks import analyze_file, ingest_document, delete_file, delete_document
from .opensearch import headers

logging.basicConfig(level=logging.INFO)


# Make elastic treat pages as nested objects
def create_mapping():
    logging.info("Creating index")

    res = requests.put(
        f"{env.get('API_ENDPOINT')}/index",
        json={"mappings": {"properties": {"pages": {"type": "nested"}}}},
        headers=headers,
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


def on_message(channel, method_frame, header_frame, body):
    body = json.loads(body)

    match method_frame.routing_key:
        case "analyze_file":
            analyze_file(body["after"])
        case "delete_file":
            delete_file(body["before"])
        case "ingest_document":
            ingest_document(body["after"])
        case "delete_document":
            delete_document(body["before"])
        case _:
            raise Exception(f"Unknown routing key: {method_frame.routing_key}")

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def on_channel_open(channel):
    channel.basic_consume("worker", on_message)


def on_open(connection):
    connection.channel(on_open_callback=on_channel_open)


def on_close(connection, exception):
    connection.ioloop.stop()


@cli.command()
def process_messages():
    create_mapping()

    # Get access token from Oauth provider
    parameters = ConnectionParameters(
        host="rabbitmq",
        credentials=PlainCredentials(
            env.get("RABBITMQ_USER"), env.get("RABBITMQ_PASSWORD")
        ),
    )

    connection = SelectConnection(
        parameters=parameters,
        on_open_callback=on_open,
        on_close_callback=on_close,
    )
    try:
        connection.ioloop.start()
    except SystemExit:
        # Gracefully close the connection
        connection.close()
        # Loop until we're fully closed.
        # The on_close callback is required to stop the io loop
        connection.ioloop.start()
