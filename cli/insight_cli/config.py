import os
from pathlib import Path
from configparser import ConfigParser

xdg_config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
config_file = xdg_config_home / "insight.conf"

config = ConfigParser()
if not config_file.exists():
    config["api"] = {
        "endpoint": "http://nginx",
    }
    config["auth"] = {
        "device-endpoint": "https://secure.ftm.nl/realms/insight/protocol/openid-connect/auth/device",
        "token-endpoint": "https://secure.ftm.nl/realms/insight/protocol/openid-connect/token",
        "client-id": "insight",
    }
    config.write(open(config_file, "w"))
else:
    config.read(config_file)
