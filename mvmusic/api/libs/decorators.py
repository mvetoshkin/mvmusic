from functools import wraps

from flask import g
from werkzeug.exceptions import Forbidden

from mvmusic.api.bp import bp


def route(rule):
    def decorator(func):
        bp.add_url_rule(rule, view_func=func, methods=("GET", "POST"))
        bp.add_url_rule(f"{rule}.view", view_func=func, methods=("GET", "POST"))
        return func

    return decorator


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.current_user:
            raise Forbidden
        return func(*args, **kwargs)

    return wrapper
