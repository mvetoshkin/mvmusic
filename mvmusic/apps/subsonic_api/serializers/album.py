from mvmusic.libs import omit_nulls
from mvmusic.models.album import Album


def album_serializer(album: Album, songs_count, duration, genres):
    resp = {
        'id': album.id_,
        'name': album.name,
        'artist': album.artist.name if album.artist else None,
        'artist_id': album.artist_id,
        'coverArt': album.image_id,
        'created': album.created_date,
        'year': album.year,
        'songCount': songs_count,
        'duration': duration,
        'genre': genres
    }

    return omit_nulls(resp, {'name', 'songCount', 'duration', 'created'})
