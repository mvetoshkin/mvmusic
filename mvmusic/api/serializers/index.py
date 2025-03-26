from mvmusic.api.serializers.artist import artist_serializer
from mvmusic.libs import omit_nulls


def index_serializer(index, starred_artists):
    resp = {
        "artist": [artist_serializer(i, starred_artists.get(i.id))
                   for i in index["artists"]],
        "name": index["name"]
    }

    return omit_nulls(resp, required={"name"})
