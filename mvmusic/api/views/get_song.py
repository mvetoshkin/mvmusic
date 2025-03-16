from flask import request
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.child import child_serializer
from mvmusic.libs.database import session
from mvmusic.models.media import Media


@route("/getSong")
@auth_required
def get_song_view():
    song_id = request.values["id"]

    try:
        media = session.get_one(Media, song_id)
    except NoResultFound:
        raise NotFound

    data = child_serializer(media)
    return make_response({"song": data})
