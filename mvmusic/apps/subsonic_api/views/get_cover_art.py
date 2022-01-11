import os

from flask import send_file
from PIL import Image as PILImage

from mvmusic.models.image import Image
from mvmusic.settings import settings
from . import BaseView


class GetCoverArtView(BaseView):
    def process_request(self, id_, size=None):
        image = Image.query.get(id_)
        orig_path = os.path.join(settings.CACHE_PATH, image.path)

        if not size:
            return send_file(orig_path, mimetype=image.mimetype)

        size = int(size)
        if size > image.height and size > image.width:
            return send_file(orig_path, mimetype=image.mimetype)

        sized_path = os.path.join(os.path.dirname(orig_path), str(size))
        if not os.path.exists(sized_path):
            with PILImage.open(orig_path) as img:
                img.thumbnail((size, size), PILImage.ANTIALIAS)
                img.save(sized_path, img.format)

        return send_file(sized_path, mimetype=image.mimetype)
