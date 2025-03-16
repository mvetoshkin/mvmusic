from pathlib import Path

from flask import g, request, send_file
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import Forbidden, NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.libs.database import session
from mvmusic.models.library import Library
from mvmusic.models.media import Media


@route("/download")
@auth_required
def download_view():
    media_id = request.values["id"]

    try:
        media = session.get_one(Media, media_id)
        library = session.get_one(Library, media.library_id)
    except NoResultFound:
        raise NotFound

    if library not in g.current_user.libraries:
        raise Forbidden

    file_path = Path(library.path) / media.path
    return send_file(file_path, mimetype=media.content_type)
