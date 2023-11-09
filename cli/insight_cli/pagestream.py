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
        headers = {"Content-Disposition": f'filename="{path.name}"'}
        res = session.post(
            f"{config['api']['endpoint']}/api/v1/pagestream",
            data=load_file(path),
            headers=headers,
        )

        if res.status_code != 201:
            exit(1)
