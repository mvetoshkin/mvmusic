from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.artist_with_albums_id3 import \
    artist_with_albums_id3_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media


@route("/getArtist")
@auth_required
def get_artist_view():
    query = select(Artist)
    query = query.options(joinedload(Artist.albums))
    query = query.join(Artist.media)
    query = query.where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Artist.id == request.values["id"]
    )

    try:
        artist = session.scalars(query).unique().one()
    except NoResultFound:
        raise NotFound

    albums_data = get_albums_data(artist)

    albums = []
    for album in artist.albums:
        album_data = albums_data[album.id]
        album_data["album"] = album
        albums.append(album_data)

    data = artist_with_albums_id3_serializer(artist, albums)
    return make_response({"artist": data})


def get_albums_data(artist):
    query = select(
        Album.id,
        func.count(Media.id.distinct()).label("songs_count"),
        func.sum(Media.duration).label("duration"),
        func.string_agg(Genre.name.distinct(), ", ").label("genres")
    )

    query = query.join(Album.media)
    query = query.outerjoin(Media.genres)
    query = query.where(Album.artist_id == artist.id)
    query = query.group_by(Album.id)

    items = {}

    for i in session.execute(query):
        items[i.id] = {
            "songs_count": i.songs_count,
            "duration": i.duration,
            "genres": i.genres
        }

    return items
