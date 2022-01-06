import json
from xml.etree import ElementTree

from flask import g

from mvmusic.libs.types import JSONEncoder
from ..libs import dict2xml
from ..libs.types import ResponseFormat


def make_response(data, status, headers=None):
    headers = headers or {}

    resp = {
        'status': 'ok' if 200 <= status < 400 else 'failed',
        'version': '1.12.0'
    }

    resp.update(data or {})

    if not hasattr(g, 'resp_format') or g.resp_format == ResponseFormat.XML:
        return make_xml_response(resp, headers), status, headers
    elif g.resp_format == ResponseFormat.JSON:
        return make_json_response(resp, headers), status, headers


def make_xml_response(resp, headers):
    headers['Content-Type'] = 'application/xml'

    root = ElementTree.Element('subsonic-response')
    dict2xml(root, resp)

    return ElementTree.tostring(root)


def make_json_response(resp, headers):
    headers['Content-Type'] = 'application/json'
    return json.dumps({'subsonic-response': resp}, cls=JSONEncoder)
