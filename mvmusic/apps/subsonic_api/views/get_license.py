from . import BaseView
from ..serializers.license import license_serializer


class GetLicenseView(BaseView):
    # noinspection PyMethodMayBeStatic
    def process_request(self):
        return {
            'license': license_serializer(True)
        }
