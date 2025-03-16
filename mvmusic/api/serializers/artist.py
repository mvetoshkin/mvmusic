from mvmusic.libs import omit_nulls


def artist_serializer(artist, starred):
    resp = {
        "id": artist.id,
        "name": artist.name,
        "starred": starred
    }

    return omit_nulls(resp, {"name"})
