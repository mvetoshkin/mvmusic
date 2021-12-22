from functools import wraps

from sqlalchemy.exc import NoResultFound

from mvmusic.common.exceptions import NotFoundError


def get_one(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        query = func(*args, **kwargs)

        try:
            record = query.one()
        except NoResultFound:
            raise NotFoundError

        return record

    return decorated_view
