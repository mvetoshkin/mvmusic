from mvmusic.libs import omit_nulls
from mvmusic.models.artist import Artist


def artist_serializer(artist: Artist, albums_count):
    resp = {
        'id': artist.id_,
        'name': artist.name,
        'albumCount': albums_count,
        'coverArt': artist.image_id
    }

    return omit_nulls(resp, {'name', 'albumCount'})
