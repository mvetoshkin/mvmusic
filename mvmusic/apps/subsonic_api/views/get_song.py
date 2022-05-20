from mvmusic.models.media import Media
from . import BaseView
from ..serializers.child import child_serializer


class GetSongView(BaseView):
    def process_request(self, id_):
        media = Media.query.get(id_)

        return {
            'song': child_serializer(media)
        }
