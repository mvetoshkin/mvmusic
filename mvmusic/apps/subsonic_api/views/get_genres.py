from sqlalchemy import func

from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.genre import genre_serializer


class GetGenresView(BaseView):
    def process_request(self):
        genres_data = self.get_genres_data()

        query = Genre.query.filter(
            Media.library_id.in_([i.id_ for i in self.user_libraries])
        )
        query = query.join(Genre.media)
        query = query.order_by(Genre.name)

        return {
            'genres': {
                'genre': [genre_serializer(i, **genres_data[i.id_])
                          for i in query.all()]
            }
        }

    def get_genres_data(self):
        query = Media.query.with_entities(
            Genre.id_,
            func.count(Media.id_.distinct()),
            func.count(Media.album_id.distinct())
        )

        query = query.join(Genre.media)
        query = query.filter(
            Media.library_id.in_([i.id_ for i in self.user_libraries])
        )
        query = query.group_by(Genre.id_)

        return {
            id_: {
                'songs_count': sc,
                'albums_count': ac
            }
            for id_, sc, ac in query.all()
        }
