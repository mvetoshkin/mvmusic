from mvmusic.api.serializers.child import child_serializer
from mvmusic.libs import omit_nulls


def album_list_serializer(albums):
    resp = {
        "album": [child_serializer(i) for i in albums]
    }

    return omit_nulls(resp)
