from mvmusic.api.serializers.genre import genre_serializer
from mvmusic.libs import omit_nulls


def genres_serializer(genres):
    resp = {
        "genre": [genre_serializer(**i) for i in genres]
    }

    return omit_nulls(resp)
