from mvmusic.api.serializers.index_id3 import index_id3_serializer
from mvmusic.libs import omit_nulls
from mvmusic.settings import SUBSONIC_API_IGNORE_ARTICLES


def artists_id3_serializer(indexes):
    resp = {
        "index": [index_id3_serializer(i) for i in indexes],
        "ignoredArticles": SUBSONIC_API_IGNORE_ARTICLES
    }

    return omit_nulls(resp, required={"ignoredArticles"})
