import json
from xml.etree import ElementTree

from flask import g

from mvmusic.api.libs import dict2xml
from mvmusic.api.libs.types import JSONEncoder
from ..serializers.response_status import reponse_status_serializer
from ..serializers.version import version_serializer


def make_response(data=None, status=200, headers=None):
    headers = headers or {}

    resp = {
        "status": reponse_status_serializer(status),
        "version": version_serializer()
    }

    resp.update(data or {})

    if not hasattr(g, "resp_format") or g.resp_format == "xml":
        return make_xml_response(resp, headers), status, headers
    elif g.resp_format == "json":
        return make_json_response(resp, headers), status, headers


def make_xml_response(resp, headers):
    headers["Content-Type"] = "application/xml"

    root = ElementTree.Element("subsonic-response")
    dict2xml(root, resp)

    return ElementTree.tostring(root)


def make_json_response(resp, headers):
    headers["Content-Type"] = "application/json"
    return json.dumps({"subsonic-response": resp}, cls=JSONEncoder)
