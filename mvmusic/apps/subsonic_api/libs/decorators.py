from functools import wraps

from mvmusic.libs.exceptions import AccessDeniedError


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]

        if not self.current_user.is_admin:
            raise AccessDeniedError

        return func(*args, **kwargs)

    return wrapper
