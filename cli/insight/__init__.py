import time
import json
import click
import os
import keyring
from requests import Session
import webbrowser
from pathlib import Path
from configparser import ConfigParser


class AuthException(Exception):
    pass


class OAuthSession(Session):
    def request(self, *args, **kwargs):
        token = load_token()
        self.headers["Authorization"] = f"Bearer {token['access_token']}"

        res = super().request(*args, **kwargs)
        if res.status_code == 401 and res.json()["message"] == "JWT expired":
            refresh_token()
            return self.request(*args, **kwargs)
        return res


xdg_config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
config_file = xdg_config_home / "insight.conf"

config = ConfigParser()
if not config_file.exists():
    config["auth"] = {
        "device-endpoint": "https://secure.ftm.nl/realms/insight/protocol/openid-connect/auth/device",
        "token-endpoint": "https://secure.ftm.nl/realms/insight/protocol/openid-connect/token",
        "client-id": "insight-cli",
    }
    config.write(open(config_file, "w"))
else:
    config.read(config_file)


def refresh_token():
    token = load_token()
    session = Session()
    data = {
        "client_id": config["auth"]["client-id"],
        "refresh_token": token["refresh_token"],
        "grant_type": "refresh_token",
    }
    res = session.post(config["auth"]["token-endpoint"], data=data)
    if res.status_code == 400 and res.json()["error"] == "invalid_grant":
        delete_token()


def delete_token():
    keyring.delete_password("insight", "insight")


def load_token():
    token = keyring.get_password("insight", "insight")
    if token is None:
        raise AuthException('Not authenticated, see "insight login"')
    return json.loads(token)


@click.group()
def cli():
    pass


@cli.command()
def login():
    data = {"client_id": config["auth"]["client-id"]}

    session = Session()
    res = session.post(config["auth"]["device-endpoint"], data=data)
    body = res.json()
    webbrowser.open(body["verification_uri_complete"])
    data["device_code"] = body["device_code"]
    data["grant_type"] = "urn:ietf:params:oauth:grant-type:device_code"

    until_time = time.time() + body["expires_in"]
    while until_time > time.time():
        res = session.post(config["auth"]["token-endpoint"], data=data)
        if res.status_code == 200:
            break
        time.sleep(body["interval"])

    keyring.set_password("insight", "insight", res.text)


@cli.command()
def logout():
    delete_token()


@cli.command()
def list_todos():
    session = OAuthSession()
    res = session.get("http://localhost:3000/todos")
    print(res.json())
