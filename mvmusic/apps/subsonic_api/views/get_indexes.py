import string
from collections import defaultdict
from datetime import datetime
from operator import attrgetter

from mvmusic.libs.exceptions import AccessDeniedError
from mvmusic.models.directory import Directory
from mvmusic.models.media import Media
from . import BaseView
from ..libs import ignored_articles
from ..serializers.indexes import indexes_serializer


class GetIndexesView(BaseView):
    def process_request(self, musicfolderid=None, ifmodifiedsince=0):
        last_modified = datetime.fromtimestamp(ifmodifiedsince / 100)
        libraries = self.user_libraries

        if musicfolderid:
            libraries = [i for i in libraries if i.id_ == musicfolderid]
            if not libraries:
                raise AccessDeniedError

        indexes, indexes_lm = self.get_indexes(libraries, last_modified)
        children, children_lm = self.get_children(libraries, last_modified)
        last_modified = max(indexes_lm, children_lm)

        return {
            'indexes': indexes_serializer(indexes, children, last_modified)
        }

    @staticmethod
    def get_indexes(libraries, last_modified):
        filters = [
            Directory.parent_id.is_(None),
            Directory.library_id.in_([i.id_ for i in libraries])
        ]

        if last_modified:
            filters.append(Directory.last_seen >= last_modified)

        indexes_raw = defaultdict(list)
        ignored = ignored_articles()
        query = Directory.query.filter(*filters)

        for item in query.all():
            name = ignored.sub('', item.name) if ignored else item.name

            index = name[0].upper()
            if index in string.digits:
                index = '#'

            indexes_raw[index].append(item)
            if not last_modified or item.last_seen > last_modified:
                last_modified = item.last_seen

        indexes = []
        for item in sorted(indexes_raw):
            indexes.append({
                'name': item,
                'artists': [i for i in sorted(
                    indexes_raw[item], key=attrgetter('name')
                )]
            })

        return indexes, last_modified

    @staticmethod
    def get_children(libraries, last_modified):
        filters = [
            Media.parent_id.is_(None),
            Media.library_id.in_([i.id_ for i in libraries])
        ]

        if last_modified:
            filters.append(Media.last_seen >= last_modified)

        children = []
        query = Media.query.filter(*filters).order_by(Media.title)

        for item in query.all():
            children.append(item)
            if not last_modified or item.last_seen > last_modified:
                last_modified = item.last_seen

        return children, last_modified
