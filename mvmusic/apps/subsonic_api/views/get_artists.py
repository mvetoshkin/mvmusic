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
        libraries = self.user_libraries

        if musicfolderid:
            libraries = [i for i in libraries if i.id_ == musicfolderid]
            if not libraries:
                raise AccessDeniedError

        resp = {
            'ignoredArticles': settings.SUBSONIC_API_IGNORE_ARTICLES
        }

        indexes = self.get_indexes(libraries)

        if indexes:
            resp['index'] = indexes

        return {
            'artists': resp
        }

    @staticmethod
    def get_indexes(libraries):
        query = Artist.query.with_entities(
            Artist,
            func.count(Album.id_.distinct())
        )
        query = query.join(Artist.albums)
        query = query.join(Artist.media)
        query = query.filter(Media.library_id.in_([i.id_ for i in libraries]))
        query = query.group_by(Artist)
        query = query.order_by(Artist.name)

        indexes_raw = defaultdict(list)
        ignored = ignored_articles()

        for item, ac in query.all():
            name = ignored.sub('', item.name) if ignored else item.name

            index = name[0].upper()
            if index in string.digits:
                index = '#'

            indexes_raw[index].append({
                'artist': item,
                'albums_count': ac
            })

        indexes = []
        for item in sorted(indexes_raw.keys()):
            indexes.append({
                'name': item,
                'artist': [
                    artist_serializer(i['artist'], i['albums_count'])
                    for i in indexes_raw[item]
                ]
            })

        return indexes
