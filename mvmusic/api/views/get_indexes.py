import string
from collections import defaultdict
from datetime import datetime
from operator import attrgetter

from flask import g, request
from sqlalchemy import select
from werkzeug.exceptions import Forbidden

from mvmusic.api.libs import ignored_articles
from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.indexes import indexes_serializer
from mvmusic.libs.database import session
from mvmusic.models.directory import Directory
from mvmusic.models.media import Media
from mvmusic.models.starred_directory import StarredDirectory


@route("/getIndexes")
@auth_required
def get_indexes_view():
    music_folder_id = request.values.get("musicFolderId")
    if_modified_since = request.values.get("ifModifiedSince", 0)

    last_modified = datetime.fromtimestamp(if_modified_since / 100)
    libraries = g.current_user.libraries

    if music_folder_id:
        libraries = [i for i in libraries if i.id == music_folder_id]
        if not libraries:
            raise Forbidden

    indexes, indexes_lm, ids = get_indexes(libraries, last_modified)
    children, children_lm = get_children(libraries, last_modified)
    last_modified = max(indexes_lm, children_lm)

    query = select(StarredDirectory).where(
        StarredDirectory.directory_id.in_(ids),
        StarredDirectory.user == g.current_user
    )

    starred_artists = {
        i.artist_id: i.created_date
        for i in session.scalars(query).unique()
    }

    data = indexes_serializer(indexes, children, last_modified, starred_artists)
    return make_response({"indexes": data})


def get_indexes(libraries, last_modified):
    query = select(Directory).where(
        Directory.parent_id.is_(None),
        Directory.library_id.in_([i.id for i in libraries])
    )

    if last_modified:
        query = query.where(Directory.last_seen >= last_modified)

    indexes_raw = defaultdict(list)
    ignored = ignored_articles()
    ids = set()

    for item in session.scalars(query):
        ids.add(item.id)
        name = ignored.sub("", item.name) if ignored else item.name

        index = name[0].upper()
        if index in string.digits:
            index = "#"

        indexes_raw[index].append(item)
        if not last_modified or item.last_seen > last_modified:
            last_modified = item.last_seen

    indexes = []
    for item in sorted(indexes_raw):
        indexes.append({
            "name": item,
            "artists": [i for i in sorted(
                indexes_raw[item], key=attrgetter("name")
            )]
        })

    return indexes, last_modified, ids


def get_children(libraries, last_modified):
    query = select(Media).where(
        Media.parent_id.is_(None),
        Media.library_id.in_([i.id for i in libraries])
    )

    if last_modified:
        query = query.where(Media.last_seen >= last_modified)

    query = query.order_by(Media.title)

    children = []

    for item in session.scalars(query).unique():
        children.append(item)
        if not last_modified or item.last_seen > last_modified:
            last_modified = item.last_seen

    return children, last_modified
