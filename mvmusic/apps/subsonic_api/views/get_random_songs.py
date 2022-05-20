from sqlalchemy import func

from mvmusic.libs.exceptions import AccessDeniedError, BadRequestError, \
    NotFoundError
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from mvmusic.models.media_genre import MediaGenre
from . import BaseView
from ..serializers.songs import songs_serializer


class GetRandomSongsView(BaseView):
    def process_request(self, size='10', genre=None, fromyear=None, toyear=None,
                        musicfolderid=None):
        size = int(size)
        size = max(size, 1)
        size = min(size, 500)

        library_ids = [i.id_ for i in self.user_libraries]
        if musicfolderid:
            if musicfolderid not in library_ids:
                raise AccessDeniedError
            library_ids = [musicfolderid]

        query = Media.query.order_by(func.random())
        query = query.filter(Media.library_id.in_(library_ids))

        if genre:
            try:
                genre_obj = Genre.query.get_by(name=genre)
            except NotFoundError:
                raise BadRequestError('Genre not found')

            query = query.join(MediaGenre)
            query = query.filter(MediaGenre.genre_id == genre_obj.id_)

        if fromyear:
            query = query.filter(Media.year >= int(fromyear))

        if toyear:
            query = query.filter(Media.year <= int(toyear))

        query = query.limit(size)
        songs = query.all()

        return {
            'randomSongs': songs_serializer(songs)
        }
