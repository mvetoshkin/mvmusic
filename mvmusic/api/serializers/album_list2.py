from mvmusic.api.serializers.album_id3 import album_id3_serializer
from mvmusic.libs import omit_nulls


def album_list2_serializer(albums):
    resp = {
        "album": [album_id3_serializer(**i) for i in albums]
    }

    return omit_nulls(resp)
