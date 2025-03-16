from mvmusic.api.serializers.child import child_serializer
from mvmusic.libs import omit_nulls


def similar_songs2_serializer(songs):
    resp = {
        "song": [child_serializer(i) for i in songs]
    }

    return omit_nulls(resp)
