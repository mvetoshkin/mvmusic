from mvmusic.api.serializers.artist import artist_serializer
from mvmusic.api.serializers.artist_info_base import artist_info_base_serializer
from mvmusic.libs import omit_nulls


def artist_info_serializer(artist, similar_artists, starred_artists):
    resp = artist_info_base_serializer(artist)
    resp["similarArtist"] = [artist_serializer(i, starred_artists.get(i.id))
                             for i in similar_artists]

    return omit_nulls(resp)
