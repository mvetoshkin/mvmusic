from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.album_with_songs_id3 import \
    album_with_songs_id3_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.media import Media


@route("/getAlbum")
@auth_required
def get_album_view():
    """Returns details for an album, including a list of songs. This method
    organizes music according to ID3 tags."""

    query = select(Album).options(
        joinedload(Album.artist),
        joinedload(Album.media).joinedload(Media.genres)
    )
    query = query.join(Album.media)
    query = query.where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Album.id == request.values["id"]
    )

    try:
        album = session.scalars(query).unique().one()
    except NoResultFound:
        raise NotFound

    genres = set()
    duration = 0

    for item in album.media:
        genres |= {i.name for i in item.genres}
        duration += item.duration or 0

    data = album_with_songs_id3_serializer(
        album, duration, ", ".join(sorted(genres)), album.media
    )

    return make_response({"album": data})
