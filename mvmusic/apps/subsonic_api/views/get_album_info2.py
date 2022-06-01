from mvmusic.models.album import Album
from . import BaseView
from ..serializers.album_info import album_info_serializer


class GetAlbumInfo2View(BaseView):
    def process_request(self, id_):
        album = Album.query.get(id_)

        return {
            'albumInfo': album_info_serializer(album)
        }
