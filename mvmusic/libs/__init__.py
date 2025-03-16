import importlib
from datetime import datetime, timezone

import requests


def import_object(path):
    module_name, object_name = path.rsplit(".", 1)
    mod = importlib.import_module(module_name)
    if not hasattr(mod, object_name):
        raise ImportError

    return getattr(mod, object_name)


def to_camel_case(text):
    text = text.replace("-", " ").replace("_", " ").lower()
    if not text:
        return text

    chunks = text.split()
    return chunks[0] + "".join(i.capitalize() for i in chunks[1:])


def omit_nulls(obj, required=None):
    required = required or set()
    required |= {"id", "value"}

    new_obj = {}

    for key, value in obj.items():
        if value is None and key not in required:
            continue
        new_obj[key] = value

    return new_obj


def dict_value(dict_: dict, path: str, default=None):
    chunks = path.split(".")

    for idx, chunk in enumerate(chunks):
        if not isinstance(dict_, dict):
            raise KeyError

        if idx == len(chunks) - 1:
            return dict_.get(chunk, default)
        else:
            dict_ = dict_.get(chunk, {})


def utcnow():
    return datetime.now(timezone.utc)


def get_request(url, params=None, **kwargs):
    headers = kwargs.get("headers", {})
    headers["User-Agent"] = ("Mozilla/5.0 (X11; Linux x86_64; rv:104.0) "
                             "Gecko/20100101 Firefox/104.0")

    return requests.get(url, params=params, headers=headers)
