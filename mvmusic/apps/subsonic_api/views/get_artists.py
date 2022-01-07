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

    def get_indexes(self, libraries):
        albums_data = self.get_albums_data(libraries)
        indexes_raw = defaultdict(list)
        ignored = ignored_articles()
        query = Artist.query.join(Artist.media).filter(
            Media.library_id.in_([i.id_ for i in libraries])
        )

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

    # noinspection PyMethodMayBeStatic
    def get_albums_data(self, libraries):
        query = Artist.query.with_entities(
            Artist.id_,
            func.count(Album.id_.distinct()),
            func.min(Media.image_id)
        )
        query = query.join(Artist.albums)
        query = query.join(Artist.media)
        query = query.filter(Media.library_id.in_([i.id_ for i in libraries]))
        query = query.group_by(Artist)

        return {
            id_: {
                'albums_count': sc,
                'media_image_id': image_id
            }
            for id_, sc, image_id in query.all()
        }
