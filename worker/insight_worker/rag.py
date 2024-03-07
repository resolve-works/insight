import httpx
import tiktoken
from os import environ as env
from itertools import islice


headers = {
    "Authorization": f"Bearer {env.get('OPENAI_API_KEY')}",
    "Content-Type": "application/json",
}

encoding = tiktoken.get_encoding("cl100k_base")


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
        Given the context information and not prior knowledge, 
        answer the query.
        Query: {query}
        Answer: 
    """

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }

    response = httpx.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=data
    )

    return response.json()["choices"][0]["message"]["content"]
