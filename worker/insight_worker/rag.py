import httpx
import tiktoken
from os import environ as env
from itertools import islice

headers = {
    "Authorization": f"Bearer {env.get('OPENAI_API_KEY')}",
    "Content-Type": "application/json",
}

encoding = tiktoken.get_encoding("cl100k_base")

SYSTEM_PROMPT = """
You are a helpful AI assistant, optimized for finding information in document
collections. You will be provided with several pages from a document
collection, and are expected to generate an answer based only on these pages,
without using any prior knowledge.
"""


# Python 3.12 itertools provide this out of the box
def batched(iterable, n):
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def embed(strings):
    for batch in batched(strings, 2048):
        # Send tokens to external service instead of the whole text
        data = {
            "input": [encoding.encode(string) for string in batch],
            "model": "text-embedding-3-small",
        }
        response = httpx.post(
            "https://api.openai.com/v1/embeddings", headers=headers, json=data
        )
        if response.status_code == 200:
            for embedding in response.json()["data"]:
                yield embedding["embedding"]
        else:
            raise Exception(response.text)


def complete(query, sources):
    context = "\n\n".join(sources)
    prompt = f"""
    Context information is below.
    ---------------------
    {context}
    ---------------------
    Given the context information and not prior knowledge, answer the query.

    Query: {query}
    Answer: 
    """

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }

    response = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(response.text())

    return response.json()["choices"][0]["message"]["content"]
