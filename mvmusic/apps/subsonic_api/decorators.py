from functools import wraps

from mvmusic.common.exceptions import AccessDeniedError


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        self = args[0]

        if not self.current_user.is_admin:
            raise AccessDeniedError

        return func(*args, **kwargs)

    return decorated_view
