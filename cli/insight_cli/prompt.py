import click
from .config import config
from .oauth import OAuthSession


@click.group()
def prompt():
    pass


@prompt.command()
def list():
    session = OAuthSession()
    res = session.get(f"{config['api']['endpoint']}/api/v1/prompt")
    print(res.json())


@prompt.command()
@click.argument("prompt")
def create(prompt):
    session = OAuthSession()
    res = session.post(
        f"{config['api']['endpoint']}/api/v1/prompt",
        json={"query": prompt},
        headers={"Prefer": "return=representation"},
    )

    if res.status_code != 201:
        exit(1)
    else:
        print(res.json()[0]["response"])
