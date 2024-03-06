from base64 import b64encode
from os import environ as env

token = b64encode(
    f"{env.get('OPENSEARCH_USER')}:{env.get('OPENSEARCH_PASSWORD')}".encode()
)
opensearch_headers = {"Authorization": f"Basic {token.decode()}"}
opensearch_endpoint = f"https://{env.get('OPENSEARCH_HOST')}:9200"
