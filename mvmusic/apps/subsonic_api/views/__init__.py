from flask import request
from flask.views import View

from mvmusic.common.exceptions import NotAllowedError
from mvmusic.common.types import RequestMethod
from ..responses import make_response


class BaseView(View):
    methods = ('GET',)

    __status = 200

    def dispatch_request(self):
        try:
            req_method = RequestMethod(request.method.lower())
            if not hasattr(self, req_method.value):
                raise ValueError
        except ValueError:
            raise NotAllowedError

        func = getattr(self, request.method.lower())
        if not func:
            raise NotAllowedError

        data = func()
        return make_response(data, self.__status)
