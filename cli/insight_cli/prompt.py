import click
from itertools import groupby
from .oauth import client
from .config import config


def print_prompts(prompts):
    for prompt in prompts:
        if "query" in prompt:
            click.echo(f"Query:    {prompt['query'].capitalize().rstrip('?')}?")
        click.echo(f"Response: {prompt['response']}")
        for file_name, pages in groupby(prompt["source"], lambda x: x.pop("name")):
            click.echo("\033[1m" + file_name.upper() + "\033[0m")
            for page in pages:
                click.echo(f"{page['score']}\t- Page {page['index'] + 1}")


@click.group()
def prompt():
    pass


@prompt.command()
def list():
    res = client.get(
        f"{config['api']['endpoint']}/api/v1/prompt?select=query,response,source(index,...file(name))"
    )
    print_prompts(res.json())


@prompt.command()
@click.argument("query")
@click.option(
    "--similarity-top-k",
    default=3,
    help="Number of pages that will be taken into the LLM context window.",
)
def create(query, similarity_top_k):
    """Prompt LLM about pages similar to the query"""
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
    print_prompts(res.json())
