from . import BaseView


class GetLicenseView(BaseView):
    # noinspection PyMethodMayBeStatic
    def process_request(self):
        return {
            'license': {
                'valid': 'true'
            }
        }
