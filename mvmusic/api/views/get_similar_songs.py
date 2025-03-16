from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.similar_songs import similar_songs_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media


@route("/getSimilarSongs")
@auth_required
def get_similar_songs_view():
    entity_id = request.values["id"]
    count = int(request.values.get("count", "20"))
    similar_songs = process_similar_songs_request(entity_id, count)
    data = similar_songs_serializer(similar_songs)
    return make_response({"similarSongs": data})


def process_similar_songs_request(entity_id, count):
    try:
        artist = session.get_one(Artist, entity_id)
        similar_songs = get_similar_by_artist(artist, count)

    except NoResultFound:
        try:
            album = session.get_one(Album, entity_id)
            similar_songs = get_similar_by_album(album, count)

        except NoResultFound:
            media = session.get_one(Media, entity_id)
            genres = [i.id for i in media.genres]
            similar_songs = get_similar_songs(genres, count)

    return similar_songs


def get_similar_by_artist(artist, count):
    genres_sq = select(Genre.id).distinct()
    genres_sq = genres_sq.join(Media.genres)
    genres_sq = genres_sq.where(Media.artist_id == artist.id)

    return get_similar_songs(genres_sq, count)


def get_similar_by_album(album, count):
    genres_sq = select(Genre.id).distinct()
    genres_sq = genres_sq.join(Media.genres)
    genres_sq = genres_sq.where(Media.album_id == album.id)

    return get_similar_songs(genres_sq, count)


def get_similar_songs(genres, count):
    query = select(Media).join(Media.genres)
    query = query.where(
        Genre.id.in_(genres),
        Media.library_id.in_({i.id for i in g.current_user.libraries})
    )
    query = query.order_by(func.random())

    if count:
        query = query.limit(count)

    return [i for i in session.scalars(query).unique()]
