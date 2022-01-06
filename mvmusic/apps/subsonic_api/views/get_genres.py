from sqlalchemy import func

from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.genre import genre_serializer


class GetGenresView(BaseView):
    def process_request(self):

        query = Media.query.with_entities(
            Genre,
            func.count(Media.id_.distinct()),
            func.count(Media.album_id.distinct())
        )

        query = query.join(Genre.media)
        query = query.filter(
            Media.library_id.in_([i.id_ for i in self.user_libraries])
        )
        query = query.group_by(Genre)
        query = query.order_by(Genre.name)

        return {
            'genres': {
                'genre': [genre_serializer(genre, sc, ac)
                          for genre, sc, ac in query.all()]
            }
        }
