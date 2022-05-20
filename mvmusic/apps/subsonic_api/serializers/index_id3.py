from mvmusic.libs import omit_nulls
from .artist_id3 import artist_id3_serializer


def index_id3_serializer(index):
    resp = {
        'artist': [artist_id3_serializer(**i) for i in index['artists']],
        'name': index['name']
    }

    return omit_nulls(resp, required={'name'})
