from mvmusic.libs import omit_nulls
from .child import child_serializer


def similar_songs_serializer(songs):
    resp = {
        'song': [child_serializer(i) for i in songs]
    }

    return omit_nulls(resp)
