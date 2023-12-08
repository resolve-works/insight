from os import environ as env
from pathlib import Path
from configparser import ConfigParser

xdg_config_home = env.get("XDG_CONFIG_HOME", Path.home() / ".config")
config_file = xdg_config_home / "insight.conf"

config = ConfigParser()
if not config_file.exists():
    config["api"] = {
        "endpoint": env.get("INSIGHT_API_ENDPOINT", "https://insight:8080"),
    }
    config["auth"] = {
        "device-endpoint": "https://secure.ftm.nl/realms/insight/protocol/openid-connect/auth/device",
        "token-endpoint": "https://secure.ftm.nl/realms/insight/protocol/openid-connect/token",
        "client-id": "insight",
    }
    config["storage"] = {
        "endpoint": "insight:9000",
        "bucket": "insight",
    }
    config.write(open(config_file, "w"))
else:
    config.read(config_file)
