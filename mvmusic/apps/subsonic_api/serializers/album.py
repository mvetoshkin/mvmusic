from mvmusic.libs import omit_nulls
from mvmusic.models.album import Album


def album_serializer(album: Album, songs_count, duration, created, year, genres,
                     media_image_id):
    resp = {
        'id': album.id_,
        'name': album.name,
        'artist': album.artist.name if album.artist else None,
        'artist_id': album.artist_id,
        'coverArt': album.image_id or media_image_id,
        'songCount': songs_count,
        'duration': duration,
        'created': created,
        'year': year,
        'genre': genres
    }

    return omit_nulls(resp, {'name', 'songCount', 'duration', 'created'})
