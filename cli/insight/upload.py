import click
from .oauth import OAuthSession


@click.group()
def upload():
    pass


@upload.command()
def list():
    session = OAuthSession()
    res = session.get("http://localhost:8080/api/v1/uploads")
    print(res.json())
