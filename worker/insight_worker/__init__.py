import click
import logging
from os import environ as env
from pika import ConnectionParameters, SelectConnection, PlainCredentials
from .ingest import analyze_file, ingest_document
from .delete import delete_document
from .oauth import OAuth2Session

logging.basicConfig(level=logging.INFO)


# Make elastic treat pages as nested objects
def create_mapping():
    logging.info("Creating index")

    res = OAuth2Session().put(
        f"{env.get('API_ENDPOINT')}/index",
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


def on_message(channel, method_frame, header_frame, body):
    logging.info(method_frame)
    logging.info(header_frame)
    logging.info(body)
    print(body)
    print()
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
        # Loop so we can communicate with RabbitMQ
        connection.ioloop.start()
    except SystemExit:
        # Gracefully close the connection
        connection.close()
        # Loop until we're fully closed.
        # The on_close callback is required to stop the io loop
        connection.ioloop.start()
