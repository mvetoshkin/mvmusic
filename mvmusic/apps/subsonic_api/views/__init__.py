import binascii
import inspect
from inspect import Signature

from flask import request
from flask.views import View

from mvmusic.common.exceptions import BadRequestError, NotFoundError, \
    UnauthorizedError
from mvmusic.models.user import User
from ..responses import make_response


class BaseView(View):
    methods = ('get', 'post',)
    current_user = None

    def dispatch_request(self):
        kwargs = self.get_kwargs()
        self.get_current_user()
        data = self.process_request(**kwargs)
        return make_response(data, 200)

    def get_current_user(self):
        username = request.values['u']
        password = request.values['p']

        if password.startswith('enc:'):
            password = binascii.unhexlify(password[4:]).decode()

        try:
            self.current_user = User.query.get_by_name(username)
            if not self.current_user.passwords_matched(password):
                raise NotFoundError

        except NotFoundError:
            raise UnauthorizedError('Wrong username or password')

    def get_kwargs(self):
        common_required = {'u', 'p', 'v', 'c', 'f'}
        required = set() | common_required
        optional = set()

        params = inspect.signature(self.process_request).parameters
        allowed = set(params)

        for param_name in params:
            if params[param_name].default == Signature.empty:
                required.add(param_name)
            else:
                optional.add(param_name)

        missing = required - set(request.values.keys())
        if missing:
            raise BadRequestError(
                'Following required parameters are missing: ' +
                ', '.join(sorted(missing))
            )

        unknown = set(request.values.keys()) - (allowed | common_required)
        if unknown:
            raise BadRequestError(
                'Following parameters are unknown: ' +
                ', '.join(sorted(unknown))
            )

        return {k: v for k, v in request.values.items()
                if k not in common_required}

    def process_request(self, *args, **kwargs):
        raise NotImplementedError
