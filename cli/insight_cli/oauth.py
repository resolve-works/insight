import json
import time
import keyring
import webbrowser
import requests
from .config import config
from oauthlib.oauth2 import DeviceClient
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from requests_oauthlib import OAuth2Session


def set_token(token):
    keyring.set_password("insight", "token", json.dumps(token))


def get_token():
    token = keyring.get_password("insight", "token")
    return json.loads(token) if token is not None else {}


def delete_token(token):
    keyring.delete_password("insight", "token")


client = OAuth2Session(
    client_id=config["auth"]["client-id"],
    token=get_token(),
    auto_refresh_url=config["auth"]["token-endpoint"],
    token_updater=set_token,
)


def authorize_device():
    res = requests.post(
        config["auth"]["device-endpoint"],
        data={"client_id": config["auth"]["client-id"]},
    )
    body = res.json()
    webbrowser.open(body["verification_uri_complete"])

    until_time = time.time() + body["expires_in"]
    while until_time > time.time():
        client = DeviceClient(config["auth"]["client-id"])
        try:
            token = OAuth2Session(client=client).fetch_token(
                client_id=config["auth"]["client-id"],
                token_url=config["auth"]["token-endpoint"],
                device_code=body["device_code"],
            )
            set_token(token)
            break
        except CustomOAuth2Error:
            time.sleep(body["interval"])
