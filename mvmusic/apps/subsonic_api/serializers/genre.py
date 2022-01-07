from mvmusic.libs import omit_nulls
from mvmusic.models.genre import Genre


def genre_serializer(genre: Genre, songs_count, albums_count):
    resp = {
        'value': genre.name,
        'songCount': songs_count,
        'albumCount': albums_count
    }

    return omit_nulls(resp, {'songCount', 'albumCount'})
