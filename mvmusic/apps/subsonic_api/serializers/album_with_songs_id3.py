from mvmusic.libs import omit_nulls
from .album_id3 import album_id3_serializer
from .child import child_serializer


def album_with_songs_id3_serializer(album, duration, genres, songs):
    resp = album_id3_serializer(album, len(songs), duration, genres)
    resp['song'] = [child_serializer(i) for i in songs]

    return omit_nulls(resp)
