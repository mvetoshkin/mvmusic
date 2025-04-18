from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.artist_info import artist_info_serializer
from mvmusic.libs.database import session
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from mvmusic.models.starred_artist import StarredArtist


@route("/getArtistInfo")
@auth_required
def get_artist_info_view():
    """Returns artist info with biography, image URLs and similar artists."""

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

    query = select(StarredArtist).where(
        StarredArtist.artist_id.in_({i.id for i in similar_artists}),
        StarredArtist.user_id == g.current_user.id
    )

    starred_artists = {
        i.artist_id: i.created_at
        for i in session.scalars(query)
    }

    data = artist_info_serializer(artist, similar_artists, starred_artists)
    return make_response({"artistInfo": data})


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

    query = select(Artist).where(Artist.id.in_(artists_sq))
    query = query.order_by(func.random())

    if count:
        query = query.limit(count)

    return [i for i in session.scalars(query)]
