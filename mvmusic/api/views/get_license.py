from mvmusic.api.libs.decorators import route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.license import license_serializer


@route("/getLicense")
def get_license_view():
    data = license_serializer(True)
    return make_response({"license": data})
