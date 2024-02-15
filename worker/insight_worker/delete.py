import logging
from os import environ as env
from .storage import get_minio
from .oauth import OAuth2Session

logging.basicConfig(level=logging.INFO)


def delete_document(id):
    session = OAuth2Session()
    res = session.get(f"{env.get('API_ENDPOINT')}/documents?id=eq.{id}")
    document = res.json()[0]

    logging.info(f"Deleting document {document['id']}")

    # Remove file from object storage
    minio = get_minio(session.token["access_token"])
    minio.remove_object(env.get("STORAGE_BUCKET"), document["path"])

    # Remove indexed contents
    res = OAuth2Session().delete(
        f"{env.get('API_ENDPOINT')}/index/_doc/{document['id']}"
    )
    if res.status_code != 200:
        raise Exception(res.text)

    # Remove indexed contents
    res = OAuth2Session().delete(
        f"{env.get('API_ENDPOINT')}/documents?id=eq.{document['id']}"
    )
    if res.status_code != 204:
        raise Exception(res.text)

    logging.info(f"Document {document['id']} deleted succesfully")
