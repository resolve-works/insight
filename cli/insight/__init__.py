import logging
from configparser import ConfigParser
import click
import os
from pathlib import Path
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import ClientSecretJWT

xdg_config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
config_file = xdg_config_home / "insight.conf"

if not config_file.exists():
    config = ConfigParser()
    config["auth"] = {
        "token_endpoint": "https://example.net/auth/realms/insight/protocol/openid-connect/token",
        "client-id": "insight",
        # "client-secret": "uIZXGkVKJjV4PIJNMyRJndQ0SGPEXRuW",
    }
    config.write(open(config_file, "w"))
    logging.error(f"Insight unconfigured, default config file written to {config_file}")
    exit(1)

config = ConfigParser()
config.read(config_file)

try:
    session = OAuth2Session(
        config["auth"]["client-id"],
        "",
        # config["auth"]["client-secret"],
        token_endpoint_auth_method=ClientSecretJWT(config["auth"]["token_endpoint"]),
    )
except KeyError:
    raise ValueError(f"Insight auth misconfigured, check [auth] in {config_file}")


@click.command()
def cli():
    click.echo("Hello World!")
