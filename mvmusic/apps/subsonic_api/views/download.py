import os

from flask import send_file

from mvmusic.libs.exceptions import AccessDeniedError
from mvmusic.models.library import Library
from mvmusic.models.media import Media
from . import BaseView


class DownloadView(BaseView):
    def process_request(self, id_):
        media = Media.query.get(id_)
        library = Library.query.get(media.library_id)

        if library not in self.user_libraries:
            raise AccessDeniedError

        file_path = os.path.join(library.path, media.path)
        return send_file(file_path, mimetype=media.content_type)
