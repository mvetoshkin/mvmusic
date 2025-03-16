from mvmusic.api.libs.decorators import route
from mvmusic.api.libs.responses import make_response


@route("/ping")
def ping_view():
    return make_response()
