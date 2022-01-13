import mimetypes
import os
import shlex
import subprocess
import tempfile

from flask import send_file

from mvmusic.libs.exceptions import AccessDeniedError
from mvmusic.models.library import Library
from mvmusic.models.media import Media
from mvmusic.settings import settings
from . import BaseView


class StreamView(BaseView):
    def process_request(self, id_, maxbitrate=None, format_=None,
                        estimatecontentlength=None):
        media = Media.query.get(id_)
        library = Library.query.get(media.library_id)

        if library not in self.user_libraries:
            raise AccessDeniedError

        file_path = os.path.join(library.path, media.path)
        content_length = media.size

        maxbitrate = int(maxbitrate) if maxbitrate else media.bitrate
        format_ = media.suffix if not format_ or format_ == 'raw' else format_

        if maxbitrate != media.bitrate or format_ != media.suffix:
            transcode_dir = os.path.join(settings.CACHE_PATH, 'transcode')
            os.makedirs(transcode_dir, exist_ok=True)

            args = shlex.split(settings.TRANSCODE_CMD.format(
                file=file_path, bitrate=maxbitrate, fmt=format_
            ))

            with tempfile.NamedTemporaryFile(dir=transcode_dir) as tmp_file, \
                    subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
                data = proc.stdout.read()
                tmp_file.write(data)
                mimetype = (mimetypes.guess_type(f'name.{format_}', False)[0] or
                            'application/octet-stream')
                content_length = len(data)
                response = send_file(tmp_file.name, mimetype=mimetype)
        else:
            response = send_file(file_path, mimetype=media.content_type)

        if str(estimatecontentlength).lower() == 'true':
            response.headers.add('Content-Length', content_length)

        return response
