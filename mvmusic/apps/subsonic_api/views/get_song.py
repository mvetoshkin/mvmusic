from mvmusic.models.media import Media
from . import BaseView
from ..serializers.media import media_serializer


class GetSongView(BaseView):
    def process_request(self, id_):
        media = Media.query.get(id_)

        return {
            'song': media_serializer(media)
        }
