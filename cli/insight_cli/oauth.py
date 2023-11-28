import json
import time
import keyring
import webbrowser
import requests
import logging
from pathlib import Path
from .config import config
from oauthlib.oauth2 import DeviceClient
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from requests_oauthlib import OAuth2Session


def set_token(token):
    try:
        keyring.set_password("insight", "token", json.dumps(token))
    except:
        logging.warning("No suitable keyring backend, storing token as plaintext!")
        with open("token.json", "w") as fh:
            fh.write(json.dumps(token))


def get_token():
    try:
        token = keyring.get_password("insight", "token")
        return json.loads(token) if token is not None else None
    except:
        try:
            with open("token.json", "r") as fh:
                logging.warning(
                    "No suitable keyring backend, reading token from plaintext!"
                )
                return json.load(fh)
        except FileNotFoundError:
            return None


def delete_token():
    try:
        keyring.delete_password("insight", "token")
    except:
        logging.warning("No suitable keyring backend, removing plaintext token file")
        Path.unlink("token.json")
        return None


client = OAuth2Session(
    client_id=config["auth"]["client-id"],
    token=get_token(),
    auto_refresh_url=config["auth"]["token-endpoint"],
    auto_refresh_kwargs={
        "client_id": config["auth"]["client-id"],
    },
    token_updater=set_token,
)


def authorize_device():
    res = requests.post(
        config["auth"]["device-endpoint"],
        data={"client_id": config["auth"]["client-id"]},
    )
    body = res.json()

    try:
        webbrowser.get()
        webbrowser.open(body["verification_uri_complete"])
    except webbrowser.Error:
        print(f"Open {body['verification_uri_complete']} to authorize this device.")

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
