from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.directory import directory_serializer
from mvmusic.libs.database import session
from mvmusic.models.directory import Directory


@route("getMusicDirectory")
@auth_required
def get_music_directory_view():
    dir_id = request.values["id"]

    query = select(Directory).where(
        Directory.id == dir_id,
        Directory.library_id.in_([i.id for i in g.current_user.libraries])
    )

    try:
        directory = session.scalars(query).one()
    except NoResultFound:
        raise NotFound

    children = [i for i in directory.children]
    children += [i for i in directory.media]

    data = directory_serializer(directory, children)
    return make_response({"directory": data})
