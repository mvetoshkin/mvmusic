from mvmusic.libs import omit_nulls
from .genre import genre_serializer


def genres_serializer(genres):
    resp = {
        'genre': [genre_serializer(**i) for i in genres]
    }

    return omit_nulls(resp)
