from . import BaseView
from .get_similar_songs import process_similar_songs_request
from ..serializers.similar_songs2 import similar_songs2_serializer


class GetSimilarSongs2View(BaseView):
    def process_request(self, id_, count='20'):
        similar_songs = process_similar_songs_request(id_, count)

        return {
            'similarSongs2': similar_songs2_serializer(similar_songs)
        }
