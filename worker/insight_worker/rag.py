import httpx
import tiktoken
from os import environ as env
from itertools import islice


# Python 3.12 itertools provide this out of the box
def batched(iterable, n):
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def embed(strings):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {env.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }
    encoding = tiktoken.get_encoding("cl100k_base")

    for batch in batched(strings, 2048):
        # Send tokens to external service instead of the whole text
        data = {
            "input": [encoding.encode(string) for string in batch],
            "model": "text-embedding-3-small",
        }
        response = httpx.post(url, headers=headers, json=data)
        if response.status_code == 200:
            for embedding in response.json()["data"]:
                yield embedding["embedding"]
        else:
            raise Exception(response.text)
