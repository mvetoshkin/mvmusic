import json

from flask import request, g

from mvmusic.common.exceptions import BadRequestError
from mvmusic.common.types import JSONEncoder
from mvmusic.subsonic_api.types import ResponseFormat


def get_resp_format():
    value = request.args.get('f', 'json')

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

    return statuses.get(status)


def make_response(data, status, headers=None):
    headers = headers or {}

    resp = {
        'subsonic-response': {
            'status': 'ok' if 200 <= status < 400 else 'failed',
            'version': '1.16.1'
        }
    }

    resp['subsonic-response'].update(data or {})

    if g.resp_format == ResponseFormat.JSON:
        return make_json_response(resp, headers), status, headers


def make_json_response(resp, headers):
    headers['Content-Type'] = 'application/json'
    return json.dumps(resp, cls=JSONEncoder)
