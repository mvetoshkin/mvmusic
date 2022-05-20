from mvmusic.libs import omit_nulls


def error_serializer(status, message):
    statuses = {
        400: 10,
        401: 40,
        403: 50,
        404: 70,
    }

    resp = {
        'code': statuses.get(status, 0),
        'message': message
    }

    return omit_nulls(resp, required={'code'})
