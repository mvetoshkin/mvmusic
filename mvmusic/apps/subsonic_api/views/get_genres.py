from sqlalchemy import func

from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.genres import genres_serializer


class GetGenresView(BaseView):
    def process_request(self):
        library_ids = [i.id_ for i in self.user_libraries]

        query = Genre.query.filter(Media.library_id.in_(library_ids))
        query = query.join(Genre.media)
        query = query.order_by(Genre.name)

        genres = []
        genres_data = self.get_genres_data(library_ids)

        for genre in query.all():
            data = genres_data[genre.id_]
            data['genre'] = genre
            genres.append(data)

        return {
            'genres': genres_serializer(genres)
        }

    @staticmethod
    def get_genres_data(library_ids):
        query = Media.query.with_entities(
            Genre.id_,
            func.count(Media.id_.distinct()).label('songs_count'),
            func.count(Media.album_id.distinct()).label('albums_count')
        )

        query = query.join(Genre.media)
        query = query.filter(Media.library_id.in_(library_ids))
        query = query.group_by(Genre.id_)

        return {i.id_: {k: i[k] for k in i.keys() if k != 'id_'}
                for i in query.all()}
