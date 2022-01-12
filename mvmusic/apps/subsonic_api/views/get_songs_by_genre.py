from mvmusic.libs.exceptions import AccessDeniedError, BadRequestError, \
    NotFoundError
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from mvmusic.models.media_genre import MediaGenre
from . import BaseView
from ..serializers.media import media_serializer


class GetSongsByGenreView(BaseView):
    def process_request(self, genre, count='10', offset='0',
                        musicfolderid=None):
        count = int(count)
        count = max(count, 1)
        count = min(count, 500)
        offset = int(offset)

        library_ids = [i.id_ for i in self.user_libraries]
        if musicfolderid:
            if musicfolderid not in library_ids:
                raise AccessDeniedError
            library_ids = [musicfolderid]

        query = Media.query.order_by(Media.created_date)
        query = query.filter(Media.library_id.in_(library_ids))

        if genre:
            try:
                genre_obj = Genre.query.get_by(name=genre)
            except NotFoundError:
                raise BadRequestError('Genre not found')

            query = query.join(MediaGenre)
            query = query.filter(MediaGenre.genre_id == genre_obj.id_)

        query = query.limit(count)
        query = query.offset(count * offset)

        return {
            'songsByGenre': [media_serializer(i) for i in query.all()]
        }
