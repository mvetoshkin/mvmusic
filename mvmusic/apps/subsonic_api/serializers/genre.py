from mvmusic.models.genre import Genre


def genre_serializer(genre: Genre, songs_count, albums_count):
    return {
        'value': genre.name,
        'songCount': songs_count,
        'albumCount': albums_count
    }
