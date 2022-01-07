from mvmusic.models.artist import Artist


def artist_serializer(artist: Artist, albums_count):
    return {
        'id': artist.id_,
        'name': artist.name,
        'coverArt': artist.image_id,
        'albumCount': albums_count
    }
