from pathlib import Path

from flask import request, send_file
from PIL import Image as PILImage
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.libs.database import session
from mvmusic.models.image import Image
from mvmusic.settings import MEDIA_PATH


@route("/getCoverArt")
@auth_required
def get_cover_art_view():
    img_id = request.values["id"]
    size = request.values.get("size")

    try:
        image = session.get_one(Image, img_id)
    except NoResultFound:
        raise NotFound

    orig_path = MEDIA_PATH / image.path

    if not size:
        return send_file(orig_path, mimetype=image.mimetype)

    size = int(size)
    if size > image.height and size > image.width:
        return send_file(orig_path, mimetype=image.mimetype)

    sized_path = Path(f"{orig_path}.{size}")

    if not sized_path.exists():
        with PILImage.open(orig_path) as img:
            img.thumbnail((size, size))
            img.save(sized_path, img.format)

    return send_file(sized_path, mimetype=image.mimetype)
