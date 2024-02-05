from os import environ as env
import requests
from minio import Minio
from xml.etree import ElementTree
from urllib.parse import urlparse


def get_minio(token):
    res = requests.post(
        env.get("STORAGE_ENDPOINT"),
        data={
            "Action": "AssumeRoleWithWebIdentity",
            "Version": "2011-06-15",
            "DurationSeconds": "3600",
            "WebIdentityToken": token,
        },
    )
    tree = ElementTree.fromstring(res.content)
    ns = {"s3": "https://sts.amazonaws.com/doc/2011-06-15/"}
    credentials = tree.find("./s3:AssumeRoleWithWebIdentityResult/s3:Credentials", ns)

    return Minio(
        urlparse(env.get("STORAGE_ENDPOINT")).netloc,
        access_key=credentials.find("s3:AccessKeyId", ns).text,
        secret_key=credentials.find("s3:SecretAccessKey", ns).text,
        session_token=credentials.find("s3:SessionToken", ns).text,
        region="insight",
    )
