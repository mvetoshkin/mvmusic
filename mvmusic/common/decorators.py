from functools import wraps

from mvmusic.common.exceptions import NotFoundError


def get_one(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        query = func(*args, **kwargs)

        record = query.first()
        if not record:
            raise NotFoundError

        return record

    return decorated_view
