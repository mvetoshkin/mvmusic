from flask import request

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.similar_songs2 import similar_songs2_serializer
from mvmusic.api.views.get_similar_songs import process_similar_songs_request


@route("/getSimilarSongs2")
@auth_required
def get_similar_songs2_view():
    """Similar to getSimilarSongs, but organizes music according to ID3 tags."""

    entity_id = request.values["id"]
    count = int(request.values.get("count", "20"))
    similar_songs = process_similar_songs_request(entity_id, count)
    data = similar_songs2_serializer(similar_songs)
    return make_response({"similarSongs2": data})
