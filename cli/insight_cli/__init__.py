import click
from .file import file
from .oauth import authorize_device, delete_token, client


@click.group()
def cli():
    """CLI for the Insight system"""
    pass


cli.add_command(file)


@cli.command()
def login():
    """Get access token from authentication provider."""
    authorize_device()


@cli.command()
def logout():
    """Remove authentication access token."""
    delete_token()


@cli.command()
def user_info():
    res = client.get(
        "https://secure.ftm.nl/realms/insight/account",
        headers={"Accept": "application/json"},
    )
    print(res.text)


@cli.command()
def user_groups():
    res = client.get(
        "https://secure.ftm.nl/realms/insight/account/groups",
        headers={"Accept": "application/json"},
    )
    print(res.text)
