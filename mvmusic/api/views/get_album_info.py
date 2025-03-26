from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api import make_response
from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.serializers.album_info import album_info_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.media import Media


@route("/getAlbumInfo")
@auth_required
def get_album_info_view():
    query = select(Album).join(Album.media)
    query = query.where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Album.id == request.values["id"]
    )

    try:
        album = session.scalars(query).unique().one()
    except NoResultFound:
        raise NotFound

    data = album_info_serializer(album)
    return make_response({"albumInfo": data})
