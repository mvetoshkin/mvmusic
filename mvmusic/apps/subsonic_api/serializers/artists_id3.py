from mvmusic.libs import omit_nulls
from mvmusic.settings import settings
from .index_id3 import index_id3_serializer


def artists_id3_serializer(indexes):
    resp = {
        'index': [index_id3_serializer(i) for i in indexes],
        'ignoredArticles': settings.SUBSONIC_API_IGNORE_ARTICLES
    }

    return omit_nulls(resp, required={'ignoredArticles'})
