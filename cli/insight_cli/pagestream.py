import click
import requests
import logging
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from pathlib import Path
from .config import config
from .oauth import OAuthSession

logging.basicConfig(level=logging.INFO)


@click.group()
def pagestream():
    pass


@pagestream.command()
def list():
    session = OAuthSession()
    res = session.get(f"{config['api']['endpoint']}/api/v1/pagestream")
    logging.info(res.json())


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
    session = OAuthSession()
    for path in files:
        res = session.post(
            f"{config['api']['endpoint']}/api/v1/rpc/create_pagestream",
            json={"name": path.name},
        )

        if res.status_code != 200:
            logging.info(res.text)
            exit(1)

        pagestream = res.json()

        with open(path, "rb") as f:
            with tqdm(
                desc=path.name,
                total=path.stat().st_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as t:
                reader_wrapper = CallbackIOWrapper(t.update, f, "read")
                res = requests.put(pagestream["url"], data=reader_wrapper)

            if res.status_code != 200:
                logging.info(res.text)
                exit(1)

        res = session.post(
            f"{config['api']['endpoint']}/api/v1/rpc/ingest_pagestream",
            json={"id": pagestream["id"]},
        )

        if res.status_code != 204:
            logging.info(res.text)
            exit(1)
