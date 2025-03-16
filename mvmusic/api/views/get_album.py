from flask import request
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.album_with_songs_id3 import \
    album_with_songs_id3_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album


@route("/getAlbum")
@auth_required
def get_album_view():
    album_id = request.values["id"]

    try:
        album = session.get_one(Album, album_id)
    except NoResultFound:
        raise NotFound

    songs = album.media.all()
    genres = set()
    duration = 0

    for item in songs:
        genres |= {i.name for i in item.genres}
        duration += item.duration or 0

    data = album_with_songs_id3_serializer(
        album, duration, ", ".join(sorted(genres)), songs
    )

    return make_response({"album": data})
