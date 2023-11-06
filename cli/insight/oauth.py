import time
import keyring
import webbrowser
from requests import Session
from .config import config


def get_access_token():
    token = keyring.get_password("insight", "access_token")
    if token is None:
        raise AuthException('Unauthenticated, run "insight login"')
    return token


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


class AuthException(Exception):
    pass


class OAuthSession(Session):
    def request(self, *args, **kwargs):
        self.headers["Authorization"] = f"Bearer {get_access_token()}"

        res = super().request(*args, **kwargs)
        if res.status_code == 401 and res.json()["message"] == "JWT expired":
            refresh_token()
            return self.request(*args, **kwargs)
        return res
