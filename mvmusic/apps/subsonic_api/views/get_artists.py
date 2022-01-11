import string
from collections import defaultdict

from sqlalchemy import func

from mvmusic.libs.exceptions import AccessDeniedError
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.media import Media
from mvmusic.settings import settings
from . import BaseView
from ..libs import ignored_articles
from ..serializers.artist import artist_serializer


class GetArtistsView(BaseView):
    def process_request(self, musicfolderid=None):
        library_ids = [i.id_ for i in self.user_libraries]

        if musicfolderid:
            if musicfolderid not in library_ids:
                raise AccessDeniedError
            library_ids = [musicfolderid]

        resp = {
            'ignoredArticles': settings.SUBSONIC_API_IGNORE_ARTICLES
        }

        indexes = self.get_indexes(library_ids)

        if indexes:
            resp['index'] = indexes

        return {
            'artists': resp
        }

    def get_indexes(self, library_ids):
        albums_data = self.get_albums_data(library_ids)
        indexes_raw = defaultdict(list)
        ignored = ignored_articles()

        query = Artist.query.join(Artist.media)
        query = query.filter(Media.library_id.in_(library_ids))

        for item in query.all():
            name = ignored.sub('', item.name) if ignored else item.name

            index = name[0].upper()
            if index in string.digits:
                index = '#'

            indexes_raw[index].append(item)

        indexes = []
        for item in sorted(indexes_raw.keys()):
            indexes.append({
                'name': item,
                'artist': [
                    artist_serializer(i, **albums_data[i.id_])
                    for i in indexes_raw[item]
                ]
            })

        return indexes

    @staticmethod
    def get_albums_data(library_ids):
        query = Artist.query.with_entities(
            Artist.id_,
            func.count(Album.id_.distinct()).label('albums_count'),
        )
        query = query.join(Artist.albums)
        query = query.join(Artist.media)
        query = query.filter(Media.library_id.in_(library_ids))
        query = query.group_by(Artist.id_)

        return {i.id_: {k: i[k] for k in i.keys() if k != 'id_'}
                for i in query.all()}
