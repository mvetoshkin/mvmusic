from mvmusic.api.serializers.artist_id3 import artist_id3_serializer
from mvmusic.api.serializers.artist_info_base import artist_info_base_serializer
from mvmusic.libs import omit_nulls


def artist_info2_serializer(artist, similar_artists):
    resp = artist_info_base_serializer(artist)
    resp["similarArtist"] = [artist_id3_serializer(**i)
                             for i in similar_artists]

    return omit_nulls(resp)
