from flask import request
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api import make_response
from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.serializers.album_info import album_info_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album


@route("/getAlbumInfo")
@auth_required
def get_album_info_view():
    album_id = request.values["id"]

    try:
        album = session.get_one(Album, album_id)
    except NoResultFound:
        return NotFound

    data = album_info_serializer(album)
    return make_response({"albumInfo": data})
