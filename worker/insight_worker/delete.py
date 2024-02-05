import logging
from os import environ as env
from .storage import get_minio
from .oauth import OAuth2Session

logging.basicConfig(level=logging.INFO)


def delete_document(id):
    session = OAuth2Session()
    res = session.get(f"{env.get('API_ENDPOINT')}/api/v1/documents?id=eq.{id}")
    document = res.json()[0]

    logging.info(f"Deleteing document {document['id']}")

    # Remove file from object storage
    minio = get_minio(session.token["access_token"])
    minio.remove_object(env.get("STORAGE_BUCKET"), document["path"])

    # Remove indexed contents
    res = OAuth2Session().delete(
        f"{env.get('API_ENDPOINT')}/api/v1/index/_doc/{document['id']}"
    )
    print(res.status_code)
    # if res.status_code != 201:
    # raise Exception(res.text)
