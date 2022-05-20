from mvmusic.libs import omit_nulls
from mvmusic.settings import settings
from .child import child_serializer
from .index import index_serializer


def indexes_serializer(indexes, children, last_modified):
    resp = {
        'index': [index_serializer(i) for i in indexes],
        'child': [child_serializer(i) for i in children],
        'lastModified': int(last_modified.timestamp() * 1000),
        'ignoredArticles': settings.SUBSONIC_API_IGNORE_ARTICLES
    }

    return omit_nulls(resp, required={'lastModified', 'ignoredArticles'})
