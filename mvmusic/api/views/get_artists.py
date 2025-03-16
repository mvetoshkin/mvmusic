import string
from collections import defaultdict

from flask import g, request
from sqlalchemy import func, select
from werkzeug.exceptions import Forbidden

from mvmusic.api.libs import ignored_articles
from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.artists_id3 import artists_id3_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.media import Media


@route("/getArtists")
@auth_required
def get_artists_view():
    music_folder_id = request.values.get("musicFolderId")

    library_ids = [i.id for i in g.current_user.libraries]

    if music_folder_id:
        if music_folder_id not in library_ids:
            raise Forbidden
        library_ids = [music_folder_id]

    indexes = get_indexes(library_ids)

    data = artists_id3_serializer(indexes)
    return make_response({"artists": data})


def get_indexes(library_ids):
    albums_data = get_albums_data(library_ids)
    indexes_raw = defaultdict(list)
    ignored = ignored_articles()

    query = select(Artist).join(Artist.media)
    query = query.where(Media.library_id.in_(library_ids))

    for item in session.scalars(query).unique():
        name = ignored.sub("", item.name) if ignored else item.name

        index = name[0].upper()
        if index in string.digits:
            index = "#"

        indexes_raw[index].append(item)

    indexes = []
    for item in sorted(indexes_raw.keys()):
        artists = []

        for artist in indexes_raw[item]:
            artist_data = albums_data[artist.id]
            artist_data["artist"] = artist
            artists.append(artist_data)

        indexes.append({
            "name": item,
            "artists": artists
        })

    return indexes


def get_albums_data(library_ids):
    query = select(
        Artist.id,
        func.count(Album.id.distinct()).label("albums_count"),
    )
    query = query.outerjoin(Artist.albums)
    query = query.outerjoin(Artist.media)
    query = query.where(Media.library_id.in_(library_ids))
    query = query.group_by(Artist.id)

    items = {}

    for i in session.execute(query):
        items[i.id] = {
            "albums_count": i.albums_count
        }

    return items
