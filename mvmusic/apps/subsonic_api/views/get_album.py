from mvmusic.models.album import Album
from . import BaseView
from ..serializers.album import album_serializer
from ..serializers.media import media_serializer


class GetAlbumView(BaseView):
    def process_request(self, id_):
        album = Album.query.get(id_)

        songs = []
        genres = set()
        duration = 0

        for item in album.media.all():
            songs.append(media_serializer(item))
            genres |= {i.name for i in item.genres}
            duration += item.duration or 0

        resp = album_serializer(
            album=album,
            songs_count=len(songs),
            duration=duration,
            genres=', '.join(sorted(genres))
        )

        resp['song'] = songs

        return {
            'album': resp
        }
