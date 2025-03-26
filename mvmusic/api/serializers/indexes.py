from mvmusic.api.serializers.child import child_serializer
from mvmusic.api.serializers.index import index_serializer
from mvmusic.libs import omit_nulls
from mvmusic.settings import SUBSONIC_API_IGNORE_ARTICLES


def indexes_serializer(indexes, children, last_modified, starred_artists):
    resp = {
        "index": [index_serializer(i, starred_artists) for i in indexes],
        "child": [child_serializer(i) for i in children],
        "lastModified": int(last_modified.timestamp() * 1000),
        "ignoredArticles": SUBSONIC_API_IGNORE_ARTICLES
    }

    return omit_nulls(resp, required={"lastModified", "ignoredArticles"})
