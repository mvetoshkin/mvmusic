from mvmusic.api.serializers.album_id3 import album_id3_serializer
from mvmusic.api.serializers.artist_id3 import artist_id3_serializer
from mvmusic.libs import omit_nulls


def artist_with_albums_id3_serializer(artist, albums):
    resp = artist_id3_serializer(artist, len(albums))
    resp["album"] = [album_id3_serializer(**i) for i in albums]

    return omit_nulls(resp)
