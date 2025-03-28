from flask import g

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.music_folders import music_folders_serializer


@route("/getMusicFolders")
@auth_required
def get_music_folders_view():
    """Returns all configured top-level music folders."""

    data = music_folders_serializer(g.current_user.libraries)
    return make_response({"musicFolders": data})
