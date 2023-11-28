from os import environ as env
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session as OAuthLibSession

client = BackendApplicationClient(client_id=env.get("AUTH_CLIENT_ID"))


class OAuth2Session(OAuthLibSession):
    def __init__(self):
        token = OAuthLibSession(client=client).fetch_token(
            token_url=env.get("AUTH_TOKEN_ENDPOINT"),
            client_secret=env.get("AUTH_CLIENT_SECRET"),
        )

        super().__init__(self, token=token)
