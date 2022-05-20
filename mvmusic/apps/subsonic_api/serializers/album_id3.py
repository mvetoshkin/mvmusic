from mvmusic.libs import omit_nulls
from mvmusic.models.album import Album


def album_id3_serializer(album: Album, songs_count, duration, genres):
    resp = {
        'id': album.id_,
        'name': album.name,
        'artist': album.artist.name if album.artist else None,
        'artistId': album.artist_id,
        'coverArt': album.image_id,
        'songCount': songs_count,
        'duration': duration,
        'created': album.created_date,
        'year': album.year,
        'genre': genres
    }

    return omit_nulls(resp, {'name', 'songCount', 'duration', 'created'})
