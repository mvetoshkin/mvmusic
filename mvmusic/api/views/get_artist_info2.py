from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api import make_response
from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.serializers.artist_info2 import artist_info2_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media


@route("/getArtistInfo2")
@auth_required
def get_artist_info2_view():
    count = int(request.values.get("count", "20"))

    query = select(Artist)
    query = query.join(Artist.media)
    query = query.where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Artist.id == request.values["id"]
    )

    try:
        artist = session.scalars(query).unique().one()
    except NoResultFound:
        raise NotFound

    similar_artists = get_similar_artists(artist, count)

    data = artist_info2_serializer(artist, similar_artists)
    return make_response({"artistInfo2": data})


def get_similar_artists(artist, count):
    genres_sq = select(Genre.id).distinct()
    genres_sq = genres_sq.join(Genre.media)
    genres_sq = genres_sq.where(Media.artist_id == artist.id)

    artists_sq = select(Media.artist_id).distinct()
    artists_sq = artists_sq.join(Media.genres)
    artists_sq = artists_sq.where(
        Genre.id.in_(genres_sq),
        Media.artist_id.isnot(None),
        Media.artist_id != artist.id,
        Media.library_id.in_([i.id for i in g.current_user.libraries])
    )

    query = select(
        Artist,
        func.count(Album.id.distinct()).label("albums_count"),
    )
    query = query.join(Artist.albums)
    query = query.where(Artist.id.in_(artists_sq))
    query = query.group_by(Artist.id)
    query = query.order_by(func.random())

    if count:
        query = query.limit(3)

    return [{"artist": i[0], "albums_count": i.albums_count}
            for i in session.execute(query)]
