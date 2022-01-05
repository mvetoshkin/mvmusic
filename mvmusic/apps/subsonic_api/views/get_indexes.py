import string
from collections import defaultdict
from datetime import datetime
from operator import attrgetter

from mvmusic.models.directory import Directory
from mvmusic.models.library import Library
from mvmusic.models.media import Media
from mvmusic.settings import settings
from . import BaseView
from ..serializers.artist import artist_serializer
from ..serializers.child import child_serializer
from ..utils import ignored_articles


class GetIndexesView(BaseView):
    def process_request(self, music_folder_id=None, if_modified_since=0):
        last_modified = datetime.fromtimestamp(if_modified_since / 100)

        libraries = self.current_user.libraries
        if music_folder_id:
            libraries = [Library.query.get(music_folder_id)]

        indexes_resp, indexes_lm = self.get_indexes(libraries, last_modified)
        children_resp, children_lm = self.get_children(libraries, last_modified)
        last_modified = max(indexes_lm, children_lm)

        return {
            'indexes': {
                'lastModified': int(last_modified.timestamp() * 1000),
                'ignoredArticles': settings.SUBSONIC_API_IGNORE_ARTICLES,
                'index': indexes_resp,
                'child': children_resp
            }
        }

    @staticmethod
    def get_indexes(libraries, last_modified):
        filters = [
            Directory.parent_id.is_(None),
            Directory.library_id.in_([i.id_ for i in libraries])
        ]

        if last_modified:
            filters.append(Directory.last_seen >= last_modified)

        indexes = defaultdict(list)
        ignored = ignored_articles()

        for d in Directory.query.filter(*filters):
            name = ignored.sub('', d.name) if ignored else d.name

            index = name[0].upper()
            if index in string.digits:
                index = '#'

            indexes[index].append(d)
            if not last_modified or d.last_seen > last_modified:
                last_modified = d.last_seen

        indexes_resp = []
        for key in sorted(indexes):
            indexes_resp.append({
                'name': key,
                'artist': [
                    artist_serializer(i)
                    for i in sorted(indexes[key], key=attrgetter('name'))
                ]
            })

        return indexes_resp, last_modified

    @staticmethod
    def get_children(libraries, last_modified):
        filters = [
            Media.parent_id.is_(None),
            Media.library_id.in_([i.id_ for i in libraries])
        ]

        if last_modified:
            filters.append(Media.last_seen >= last_modified)

        children_resp = []

        for m in Media.query.filter(*filters).order_by(Media.title):
            children_resp.append(child_serializer(m))
            if not last_modified or m.last_seen > last_modified:
                last_modified = m.last_seen

        return children_resp, last_modified
