from flask.views import View

from ..responses import make_response


class BaseView(View):
    methods = ('get', 'post',)
    current_user = None

    def dispatch_request(self):
        data = self.process_request()
        return make_response(data, 200)

    def process_request(self):
        raise NotImplementedError
