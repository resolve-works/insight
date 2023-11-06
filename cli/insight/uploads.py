import click
from .oauth import OAuthSession


@click.group()
def uploads():
    pass


@uploads.command()
def list():
    session = OAuthSession()
    res = session.get("http://localhost:8080/api/v1/uploads")
    print(res.json())


@uploads.command()
@click.argument("files", nargs=-1, type=click.File("rb"))
def create(files):
    session = OAuthSession()
    for file in files:
        res = session.post("http://localhost:8080/api/v1/uploads", data=file)

        if res.status_code != 201:
            click.echo(res.text)
            exit(1)
