import click
from itertools import groupby
from .config import config
from .pagestream import pagestream
from .oauth import authorize_device, delete_token, client


@click.group()
def cli():
    """CLI for the Insight system"""
    pass


cli.add_command(pagestream)


@cli.command()
def login():
    """Get access token from authentication provider."""
    authorize_device()


@cli.command()
def logout():
    """Remove authentication access token."""
    delete_token()


@cli.command()
@click.argument("query")
def search(query):
    """Search pages for text."""
    body = {
        "_source": {"excludes": ["insight:pages"]},
        "query": {
            "nested": {
                "path": "insight:pages",
                "query": {"match": {"insight:pages.contents": query}},
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

    res = client.get(f"{config['api']['endpoint']}/api/v1/index/_search", json=body)
    if res.status_code != 200:
        click.echo(res.status_code)
        exit(1)

    for file in res.json()["hits"]["hits"]:
        click.echo("\033[1m" + file["_source"]["insight:filename"].upper() + "\033[0m")
        for page in file["inner_hits"]["insight:pages"]["hits"]["hits"]:
            click.echo(f"Page {page['_source']['index'] + 1}")
            for highlight in page["highlight"]["insight:pages.contents"]:
                highlight = highlight.replace("\n", "")
                click.echo(f"\t{highlight}")


@cli.command()
@click.argument("query")
@click.option(
    "--similarity-top-k",
    default=3,
    help="Number of pages that will be taken into the LLM context window.",
)
def prompt(query, similarity_top_k):
    """Query LLM about pages similar to a prompt."""
    res = client.post(
        f"{config['api']['endpoint']}/api/v1/rpc/create_prompt",
        data={"query": query, "similarity_top_k": similarity_top_k},
        headers={"Prefer": "return=representation"},
    )

    if res.status_code != 200:
        print(res.text)
        exit(1)

    res = client.get(
        f"{config['api']['endpoint']}/api/v1/prompt?select=response,source(score, index,...file(name))&source.order=score.desc&id=eq.{res.json()[0]['id']}"
    )

    for prompt in res.json():
        click.echo(f"Response: {prompt['response']}")
        for file_name, pages in groupby(prompt["source"], lambda x: x.pop("name")):
            click.echo("\033[1m" + file_name.upper() + "\033[0m")
            for page in pages:
                click.echo(f"{page['score']}\t- Page {page['index'] + 1}")
