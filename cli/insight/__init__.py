import time
import click
import os
import keyring
from requests import Session
import webbrowser
from pathlib import Path
from configparser import ConfigParser


class AuthException(Exception):
    pass


def set_tokens(data):
    for token in ("refresh_token", "access_token"):
        keyring.set_password("insight", token, data[token])


def delete_tokens():
    for token in ("refresh_token", "access_token"):
        try:
            keyring.delete_password("insight", token)
        except keyring.errors.PasswordDeleteError:
            pass


def authorize_device():
    session = Session()
    res = session.post(
        config["auth"]["device-endpoint"],
        data={"client_id": config["auth"]["client-id"]},
    )
    body = res.json()
    webbrowser.open(body["verification_uri_complete"])

    until_time = time.time() + body["expires_in"]
    while until_time > time.time():
        res = session.post(
            config["auth"]["token-endpoint"],
            data={
                "client_id": config["auth"]["client-id"],
                "device_code": body["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )
        if res.status_code == 200:
            break
        time.sleep(body["interval"])

    if res.status_code == 200:
        set_tokens(res.json())
    else:
        raise Exception(res.text)


def refresh_token():
    session = Session()
    res = session.post(
        config["auth"]["token-endpoint"],
        data={
            "client_id": config["auth"]["client-id"],
            "refresh_token": keyring.get_password("insight", "refresh_token"),
            "grant_type": "refresh_token",
        },
    )
    if res.status_code == 200:
        set_tokens(res.json())
    else:
        delete_tokens()
        raise Exception(res.text)


class OAuthSession(Session):
    def request(self, *args, **kwargs):
        token = keyring.get_password("insight", "access_token")
        if token is None:
            raise AuthException('Unauthenticated, run "insight login"')

        self.headers["Authorization"] = f"Bearer {token}"

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


@click.group()
def cli():
    pass


@cli.command()
def login():
    authorize_device()


@cli.command()
def logout():
    delete_tokens()


@click.group()
def files():
    pass


@files.command()
def list():
    session = OAuthSession()
    res = session.get("http://localhost:3000/files")
    print(res.json())


cli.add_command(files)
