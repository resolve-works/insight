import click
import requests
import logging
from minio import Minio
from xml.etree import ElementTree
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from pathlib import Path
from .config import config
from .oauth import client, get_token


@click.group()
def file():
    """Manage PDF files."""
    pass


@file.command()
def list():
    """List uploaded PDF files."""
    res = client.get(f"{config['api']['endpoint']}/api/v1/files")
    print(res.text)


def load_file(path):
    progressbar = tqdm(
        desc=path.name,
        total=path.stat().st_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    )

    for chunk in iter(open(path, "rb")):
        progressbar.update(len(chunk))
        yield chunk


@file.command()
@click.argument("files", nargs=-1, type=click.Path(path_type=Path))
def upload(files):
    """Ingest PDF files"""

    for path in files:
        res = client.post(
            f"{config['api']['endpoint']}/api/v1/files",
            data={"name": path.name},
            headers={"Prefer": "return=representation"},
        )

        if res.status_code != 201:
            logging.error(res.text)
            exit(1)

        file = res.json()[0]
        size = path.stat().st_size

        with open(path, "rb") as f:
            with tqdm(
                desc=path.name,
                total=size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as t:
                reader_wrapper = CallbackIOWrapper(t.update, f, "read")

                res = requests.post(
                    f"https://{config['storage']['endpoint']}",
                    data={
                        "Action": "AssumeRoleWithWebIdentity",
                        "Version": "2011-06-15",
                        "DurationSeconds": "3600",
                        "WebIdentityToken": get_token()["access_token"],
                    },
                )
                tree = ElementTree.fromstring(res.content)
                ns = {"s3": "https://sts.amazonaws.com/doc/2011-06-15/"}
                credentials = tree.find(
                    "./s3:AssumeRoleWithWebIdentityResult/s3:Credentials", ns
                )

                minio = Minio(
                    config["storage"]["endpoint"],
                    access_key=credentials.find("s3:AccessKeyId", ns).text,
                    secret_key=credentials.find("s3:SecretAccessKey", ns).text,
                    session_token=credentials.find("s3:SessionToken", ns).text,
                    region="insight",
                )

                minio.put_object(
                    config["storage"]["bucket"],
                    file["path"],
                    reader_wrapper,
                    size,
                    content_type="application/pdf",
                )

                # TODO - trigger ingest

                if res.status_code != 204:
                    logging.error(res.text)
                    exit(1)
