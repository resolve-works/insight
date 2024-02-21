from os import environ as env
from minio import Minio
from urllib.parse import urlparse


def get_minio():
    return Minio(
        urlparse(env.get("STORAGE_ENDPOINT")).netloc,
        access_key=env.get("STORAGE_ACCESS_KEY"),
        secret_key=env.get("STORAGE_SECRET_KEY"),
        region="insight",
    )
