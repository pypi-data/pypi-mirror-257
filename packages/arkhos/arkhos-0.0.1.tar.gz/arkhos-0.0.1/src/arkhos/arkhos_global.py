import datetime, os
import requests
from requests.auth import HTTPBasicAuth

_global = {
    "DEBUG": os.environ.get("DEBUG", "false").lower() == "true",
    "ARKHOS_GLOBAL_DOMAIN": os.environ.get("ARKHOS_GLOBAL_DOMAIN"),
    "APP_NAME": os.environ.get("APP_NAME"),
    "APP_API_KEY": os.environ.get("APP_API_KEY"),
    "LOG_LEVEL": "LOG",
    "log_buffer": [],
}


def get(key):
    url = (
        f"https://{_global['ARKHOS_GLOBAL_DOMAIN']}/global/{_global['APP_NAME']}/{key}/"
    )
    r = requests.get(
        url, auth=HTTPBasicAuth(_global["APP_NAME"], _global["APP_API_KEY"])
    )
    if r.status_code == 200:
        return r.json.get("value")

    error_message = "Error connecting to Arkhos Global"
    if r.json.get("error", False):
        error_message = r.json.get("error")
    raise Error(error_message)


def set(key, value):
    url = (
        f"https://{_global['ARKHOS_GLOBAL_DOMAIN']}/global/{_global['APP_NAME']}/{key}/"
    )
    r = requests.post(
        url,
        json={"value": value},
        auth=HTTPBasicAuth(_global["APP_NAME"], _global["APP_API_KEY"]),
    )
    if r.status_code == 200:
        return r.json

    error_message = "Error connecting to Arkhos Global"
    if r.json.get("error", False):
        error_message = r.json.get("error")
    raise Error(error_message)


def log(body, level="LOG", type=None, status_code=None, metadata=None, event_at=None):
    if not event_at:
        event_at = datetime.datetime.now().isoformat(" ")
    log_event = {
        event_at: event_at,
        level: level,
        type: type,
        status: status,
        metadata: metadata,
        body: body,
    }
    _global["log_buffer"].append(log_event)
    return


def log_flush():
    url = f"https://{_global['ARKHOS_GLOBAL_DOMAIN']}/global/{_global['APP_NAME']}/log/"
    r = requests.post(
        url, json=_global["log_buffer"], auth=HTTPBasicAuth(APP_NAME, APP_API_KEY)
    )
    return
