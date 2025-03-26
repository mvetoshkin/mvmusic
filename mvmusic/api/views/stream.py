import mimetypes
import os
import shlex
import subprocess
import tempfile
from pathlib import Path

from flask import g, request, send_file
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.libs.database import session
from mvmusic.models.media import Media
from mvmusic.settings import CACHE_PATH, TRANSCODE_CMD


@route("stream")
@auth_required
def stream_view():
    query = select(Media).options(joinedload(Media.library))
    query = query.where(Media.id == request.values["id"])

    try:
        media = session.scalars(query).one()
    except NoResultFound:
        raise NotFound

    if media.library not in g.current_user.libraries:
        raise NotFound

    max_bitrate = request.values.get("maxBitRace")
    fmt = request.values.get("format")
    estimate_content_length = request.values.get(
        "estimateContentLength", "false"
    )

    file_path = Path(media.library.path) / media.path
    content_length = media.size

    max_bitrate = int(max_bitrate) if max_bitrate else media.bitrate
    fmt = file_path.suffix[1:] if not fmt or fmt == "raw" else fmt

    if max_bitrate != media.bitrate or fmt != file_path.suffix[1:]:
        transcode_dir = CACHE_PATH / "transcode"
        os.makedirs(transcode_dir, exist_ok=True)

        args = shlex.split(TRANSCODE_CMD.format(
            file=file_path, bitrate=max_bitrate, fmt=fmt
        ))

        with tempfile.NamedTemporaryFile(dir=transcode_dir) as tmp_file, \
                subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
            data = proc.stdout.read()
            tmp_file.write(data)
            mimetype = (mimetypes.guess_type(f"name.{fmt}", False)[0] or
                        "application/octet-stream")
            content_length = len(data)
            response = send_file(tmp_file.name, mimetype=mimetype)

    else:
        response = send_file(file_path, mimetype=media.content_type)

    if str(estimate_content_length).lower() == "true":
        response.headers.add("Content-Length", content_length)

    return response
