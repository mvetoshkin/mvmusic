from mvmusic.models.album import Album
from . import BaseView
from ..serializers.album_with_songs_id3 import album_with_songs_id3_serializer


class GetAlbumView(BaseView):
    def process_request(self, id_):
        album = Album.query.get(id_)
        songs = album.media.all()

        genres = set()
        duration = 0

        for item in songs:
            genres |= {i.name for i in item.genres}
            duration += item.duration or 0

        return {
            'album': album_with_songs_id3_serializer(
                album, duration, ', '.join(sorted(genres)), songs
            )
        }
