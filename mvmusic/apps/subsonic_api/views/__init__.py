import binascii
import inspect
from inspect import Signature

from flask import request, Response
from flask.views import View

from mvmusic.libs.exceptions import AccessDeniedError, BadRequestError, \
    NotFoundError, UnauthorizedError
from mvmusic.models.library import Library
from mvmusic.models.user import User
from ..libs.responses import make_response


class BaseView(View):
    methods = ('get', 'post',)
    current_user = None

    @property
    def user_libraries(self):
        libraries = Library.query.all() if self.current_user.is_admin \
            else self.current_user.libraries

        if not libraries:
            raise AccessDeniedError('User does not have any libraries')

        return libraries

    def dispatch_request(self):
        kwargs = self.get_kwargs()
        self.get_current_user()
        data = self.process_request(**kwargs)

        if isinstance(data, Response):
            return data

        return make_response(data, 200)

    def get_current_user(self):
        username = request.values['u']
        password = request.values['p']

        if password.startswith('enc:'):
            password = binascii.unhexlify(password[4:]).decode()

        try:
            self.current_user = User.query.get_by(username=username)
            if not self.current_user.passwords_matched(password):
                raise NotFoundError

        except NotFoundError:
            raise UnauthorizedError('Wrong username or password')

    def get_kwargs(self):
        builtin_names = ('id', 'format',)

        common_required = {'u', 'p', 'v', 'c'}
        common_optional = {'f'}
        required = set() | common_required
        optional = set() | common_optional

        params = inspect.signature(self.process_request).parameters
        allowed = set(params)

        for param_name in params:
            if params[param_name].default == Signature.empty:
                required.add(param_name)
            else:
                optional.add(param_name)

        req_attrs = set()
        for attr in request.values.keys():
            attr = attr.lower()
            if attr in builtin_names:
                attr += '_'
            req_attrs.add(attr)

        missing = required - req_attrs
        if missing:
            raise BadRequestError(
                'Following required parameters are missing: ' +
                ', '.join(sorted(missing))
            )

        unknown = req_attrs - (allowed | common_required | common_optional)
        if unknown:
            raise BadRequestError(
                'Following parameters are unknown: ' +
                ', '.join(sorted(unknown))
            )

        attrs = {}
        for k, v in request.values.items():
            attr = k.lower()
            if attr in common_required or attr in common_optional:
                continue

            if attr in builtin_names:
                attr += '_'

            attrs[attr] = v

        return attrs

    def process_request(self, *args, **kwargs):
        raise NotImplementedError
