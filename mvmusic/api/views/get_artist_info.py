from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api import make_response
from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.serializers.artist_info import artist_info_serializer
from mvmusic.libs.database import session
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from mvmusic.models.starred_artist import StarredArtist


@route("/getArtistInfo")
@auth_required
def get_artist_info_view():
    artist_id = request.values["id"]
    count = int(request.values.get("count", "20"))

    try:
        artist = session.get_one(Artist, artist_id)
    except NoResultFound:
        return NotFound

    similar_artists = get_similar_artists(artist, count)

    query = select(StarredArtist).where(
        StarredArtist.artist_id.in_({i.id for i in similar_artists}),
        StarredArtist.user == g.current_user
    )

    starred_artists = {
        i.artist_id: i.created_at
        for i in session.scalars(query)
    }

    data = artist_info_serializer(artist, similar_artists, starred_artists)
    return make_response({"artistInfo": data})


def get_similar_artists(artist, count):
    genres_sq = select(Genre.id).distinct()
    genres_sq = genres_sq.join(Media.genres)
    genres_sq = genres_sq.where(Media.artist_id == artist.id)

    artists_sq = select(Media.artist_id).distinct()
    artists_sq = artists_sq.join(Media.genres)
    artists_sq = artists_sq.where(
        Genre.id.in_(genres_sq),
        Media.artist_id != artist.id,
        Media.library_id.in_({i.id for i in g.current_user.libraries})
    )

    if count:
        artists_sq = artists_sq.limit(count)

    query = select(Artist).where(Artist.id.in_(artists_sq))
    return [i for i in session.scalars(query)]
