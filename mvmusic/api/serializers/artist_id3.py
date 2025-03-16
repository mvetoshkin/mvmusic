from mvmusic.libs import omit_nulls


def artist_id3_serializer(artist, albums_count):
    resp = {
        "id": artist.id,
        "name": artist.name,
        "coverArt": artist.image_id,
        "albumCount": albums_count
    }

    return omit_nulls(resp, {"name", "albumCount"})
