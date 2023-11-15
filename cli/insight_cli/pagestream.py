import click
from tqdm import tqdm
from pathlib import Path
from .config import config
from .oauth import OAuthSession


@click.group()
def pagestream():
    pass


@pagestream.command()
def list():
    session = OAuthSession()
    res = session.get(f"{config['api']['endpoint']}/api/v1/pagestream")
    print(res.json())


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
            headers={"Prefer": "return=representation"},
        )

        if res.status_code != 201:
            print(res.text)
            exit(1)
        else:
            print(res.json())
