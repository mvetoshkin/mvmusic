import json
from xml.etree import ElementTree

from flask import g, request

from mvmusic.common.exceptions import BadRequestError
from mvmusic.common.types import JSONEncoder
from .types import ResponseFormat


def get_resp_format():
    value = request.values.get('f', 'xml')

    try:
        g.resp_format = ResponseFormat(value)
    except ValueError:
        raise BadRequestError('Format not supported')


def get_subsonic_error_code(status):
    statuses = {
        400: 10,
        401: 40,
        403: 50,
        404: 70,
    }

    return statuses.get(status, 0)


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


def dict2xml(element, dictionary):
    for name, value in dictionary.items():
        if name == 'value':
            element.text = value_tostring(value)

        elif isinstance(value, dict):
            sub_element = ElementTree.SubElement(element, name)
            dict2xml(sub_element, value)

        elif isinstance(value, list):
            for v in value:
                sub_element = ElementTree.SubElement(element, name)

                if isinstance(v, dict):
                    dict2xml(sub_element, v)
                else:
                    sub_element.text = value_tostring(v)

        else:
            element.set(name, value_tostring(value))


def value_tostring(value):
    if value is None:
        return None

    if isinstance(value, str):
        return value

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def make_json_response(resp, headers):
    headers['Content-Type'] = 'application/json'
    return json.dumps({'subsonic-response': resp}, cls=JSONEncoder)
