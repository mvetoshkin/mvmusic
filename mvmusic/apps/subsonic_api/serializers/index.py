from mvmusic.libs import omit_nulls
from .artist import artist_serializer


def index_serializer(index):
    resp = {
        'artist': [artist_serializer(i) for i in index['artists']],
        'name': index['name']
    }

    return omit_nulls(resp, required={'name'})
