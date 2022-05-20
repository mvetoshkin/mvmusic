from mvmusic.libs import omit_nulls


def artist_serializer(artist):
    resp = {
        'id': artist.id_,
        'name': artist.name
    }

    return omit_nulls(resp, {'name'})
