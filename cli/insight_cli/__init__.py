import click
import requests
from .config import config
from .pagestream import pagestream
from .oauth import OAuthSession, authorize_device, delete_tokens


@click.group()
def cli():
    pass


cli.add_command(pagestream)


@cli.command()
def login():
    authorize_device()


@cli.command()
def logout():
    delete_tokens()


@cli.command()
@click.argument("query")
def prompt(query):
    session = OAuthSession()
    res = session.post(
        f"{config['api']['endpoint']}/api/v1/rpc/create_prompt",
        json={"query": query},
        headers={"Prefer": "return=representation"},
    )

    if res.status_code != 200:
        exit(1)
    else:
        print(res.json())


@cli.command()
@click.argument("string")
def search(string):
    body = {
        "_source": {"excludes": ["insight:pages"]},
        "query": {
            "nested": {
                "path": "insight:pages",
                "query": {"match": {"insight:pages.contents": string}},
                "inner_hits": {
                    "highlight": {
                        "pre_tags": ["\033[1m"],
                        "post_tags": ["\033[0m"],
                        "fields": {"insight:pages.contents": {}},
                    },
                },
            },
        },
    }

    res = requests.get(f"{config['api']['endpoint']}/api/v1/search", json=body)

    for file in res.json()["hits"]["hits"]:
        click.echo("\033[1m" + file["_source"]["insight:filename"].upper() + "\033[0m")
        for page in file["inner_hits"]["insight:pages"]["hits"]["hits"]:
            click.echo(f"Page {page['_source']['index'] + 1}")
            for index, highlight in enumerate(
                page["highlight"]["insight:pages.contents"]
            ):
                highlight = highlight.replace("\n", "")
                click.echo(f"\t{index} - {highlight}")
