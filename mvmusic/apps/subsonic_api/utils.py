import re

from mvmusic.settings import settings


def ignored_articles():
    ignored = settings.SUBSONIC_API_IGNORE_ARTICLES
    if not ignored:
        return None

    chunks = ignored.split(' ')
    reg_exp = '^(' + ' |'.join(re.escape(i) for i in chunks) + ')'

    return re.compile(reg_exp, re.IGNORECASE)
