import click
from .oauth import OAuthSession
from .config import config


@click.group()
def prompt():
    pass


@prompt.command()
def list():
    session = OAuthSession()
    res = session.get(f"{config['api']['endpoint']}/api/v1/prompt?select=*,source(*)")
    print(res.text)


@prompt.command()
@click.argument("query")
def create(query):
    session = OAuthSession()
    res = session.post(
        f"{config['api']['endpoint']}/api/v1/rpc/create_prompt",
        json={"query": query},
        headers={"Prefer": "return=representation"},
    )

    if res.status_code != 200:
        exit(1)

    session = OAuthSession()
    res = session.get(
        f"{config['api']['endpoint']}/api/v1/prompt?select=*,source(*)&id=eq.{res.json()[0]['id']}"
    )
    print(res.text)
