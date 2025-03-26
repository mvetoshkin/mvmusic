from pathlib import Path

from flask import g, request, send_file
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.libs.database import session
from mvmusic.models.media import Media


@route("/download")
@auth_required
def download_view():
    query = select(Media).options(joinedload(Media.library))
    query = query.where(Media.id == request.values["id"])

    try:
        media = session.scalars(query).one()
    except NoResultFound:
        raise NotFound

    if media.library not in g.current_user.libraries:
        raise NotFound

    file_path = Path(media.library.path) / media.path
    return send_file(file_path, mimetype=media.content_type)
