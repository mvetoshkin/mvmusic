from mvmusic.libs import omit_nulls
from .artist_info_base import artist_info_base_serializer
from .artist import artist_serializer


def artist_info_serializer(artist, similar_artists):
    resp = artist_info_base_serializer(artist)
    resp['similarArtist'] = [artist_serializer(i) for i in similar_artists]

    return omit_nulls(resp)
