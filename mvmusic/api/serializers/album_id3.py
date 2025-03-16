from mvmusic.libs import omit_nulls


def album_id3_serializer(album, songs_count, duration, genres):
    resp = {
        "id": album.id,
        "name": album.name,
        "artist": album.artist.name if album.artist else None,
        "artistId": album.artist_id,
        "coverArt": album.image_id,
        "songCount": songs_count,
        "duration": duration,
        "created": album.created_at,
        "year": album.year,
        "genre": genres
    }

    return omit_nulls(resp, {"name", "songCount", "duration", "created"})
