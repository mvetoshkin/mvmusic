from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.child import child_serializer
from mvmusic.libs.database import session
from mvmusic.models.media import Media


@route("/getSong")
@auth_required
def get_song_view():
    query = select(Media).options(
        joinedload(Media.artist),
        joinedload(Media.album),
        joinedload(Media.genres),
    )
    query = query.where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Media.id == request.values["id"]
    )

    try:
        media = session.scalars(query).unique().one()
    except NoResultFound:
        raise NotFound

    data = child_serializer(media)
    return make_response({"song": data})
