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
def pagestream():
    """Manage PDF pagestreams."""
    pass


@pagestream.command()
def list():
    """List uploaded PDF pagestreams."""
    res = client.get(f"{config['api']['endpoint']}/api/v1/pagestream")
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


@pagestream.command()
@click.argument("files", nargs=-1, type=click.Path(path_type=Path))
def create(files):
    """Ingest PDF pagestreams"""

    for path in files:
        res = client.post(
            f"{config['api']['endpoint']}/api/v1/pagestreams",
            data={"name": path.name},
            headers={"Prefer": "return=representation"},
        )

        if res.status_code != 201:
            logging.error(res.text)
            exit(1)

        pagestream = res.json()[0]
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
                    pagestream["path"],
                    reader_wrapper,
                    size,
                    content_type="application/pdf",
                )

                res = client.patch(
                    f"{config['api']['endpoint']}/api/v1/pagestreams?id=eq.{pagestream['id']}",
                    data={"status": "idle"},
                )

                if res.status_code != 204:
                    logging.error(res.text)
                    exit(1)

                res = client.post(
                    f"{config['api']['endpoint']}/api/v1/rpc/ingest_pagestream",
                    data={"id": pagestream["id"]},
                )

                if res.status_code != 204:
                    logging.error(res.text)
                    exit(1)
