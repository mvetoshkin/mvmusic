from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

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
    """Returns a random collection of songs from the given artist and
    similar artists. Typically used for artist radio features."""

    entity_id = request.values["id"]
    count = int(request.values.get("count", "20"))
    similar_songs = process_similar_songs_request(entity_id, count)
    data = similar_songs_serializer(similar_songs)
    return make_response({"similarSongs": data})


def process_similar_songs_request(entity_id, count):
    library_ids = [i.id for i in g.current_user.libraries]

    try:
        query = select(Artist.id).distinct().join(Artist.media)
        query = query.where(
            Artist.id == entity_id,
            Media.library_id.in_(library_ids)
        )

        artist_id = session.scalars(query).one()
        similar_songs = get_similar_by_artist(artist_id, count)

    except NoResultFound:
        try:
            query = select(Album.id).distinct().join(Album.media)
            query = query.where(
                Album.id == entity_id,
                Media.library_id.in_(library_ids)
            )

            album_id = session.scalars(query).one()
            similar_songs = get_similar_by_album(album_id, count)

        except NoResultFound:
            query = select(Media).options(joinedload(Media.genres))
            query = query.where(
                Media.id == entity_id,
                Media.library_id.in_(library_ids)
            )

            media = session.scalars(query).one()
            genres = [i.id for i in media.genres]
            similar_songs = get_similar_songs(genres, count)

    return similar_songs


def get_similar_by_artist(artist_id, count):
    genres_sq = select(Genre.id).distinct()
    genres_sq = genres_sq.join(Genre.media)
    genres_sq = genres_sq.where(Media.artist_id == artist_id)

    return get_similar_songs(genres_sq, count)


def get_similar_by_album(album_id, count):
    genres_sq = select(Genre.id).distinct()
    genres_sq = genres_sq.join(Genre.media)
    genres_sq = genres_sq.where(Media.album_id == album_id)

    return get_similar_songs(genres_sq, count)


def get_similar_songs(genres, count):
    query = select(Media).options(
        joinedload(Media.artist),
        joinedload(Media.album),
        joinedload(Media.genres)
    )
    query = query.join(Media.genres)
    query = query.where(
        Genre.id.in_(genres),
        Media.library_id.in_([i.id for i in g.current_user.libraries])
    )
    query = query.order_by(func.random())

    if count:
        query = query.limit(count)

    return [i for i in session.scalars(query).unique()]
