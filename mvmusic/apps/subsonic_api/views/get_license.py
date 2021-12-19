from . import BaseView


class GetLicenseView(BaseView):
    # noinspection PyMethodMayBeStatic
    def get(self):
        return {
            'license': {
                'valid': 'true'
            }
        }
