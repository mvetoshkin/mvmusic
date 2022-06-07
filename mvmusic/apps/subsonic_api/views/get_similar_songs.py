from sqlalchemy import func

from mvmusic.libs.exceptions import NotFoundError
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.similar_songs import similar_songs_serializer


class GetSimilarSongsView(BaseView):
    def process_request(self, id_, count='20'):
        similar_songs = process_similar_songs_request(id_, count)

        return {
            'similarSongs': similar_songs_serializer(similar_songs)
        }


def process_similar_songs_request(id_, count):
    count = int(count)

    try:
        artist = Artist.query.get(id_)
        similar_songs = get_similar_by_artist(artist, count)
    except NotFoundError:
        try:
            album = Album.query.get(id_)
            similar_songs = get_similar_by_album(album, count)
        except NotFoundError:
            media = Media.query.get(id_)
            genres = [i.id_ for i in media.genres]
            similar_songs = get_similar_songs(genres, count)

    return similar_songs


def get_similar_by_artist(artist, count):
    genres_sq = Genre.query.with_entities(Genre.id_).distinct()
    genres_sq = genres_sq.join(Media.genres)
    genres_sq = genres_sq.filter(Media.artist == artist)

    return get_similar_songs(genres_sq, count)


def get_similar_by_album(album, count):
    genres_sq = Genre.query.with_entities(Genre.id_).distinct()
    genres_sq = genres_sq.join(Media.genres)
    genres_sq = genres_sq.filter(Media.album == album)

    return get_similar_songs(genres_sq, count)


def get_similar_songs(genres, count):
    query = Media.query.join(Media.genres)
    query = query.filter(Genre.id_.in_(genres))
    query = query.order_by(func.random())

    if count:
        query = query.limit(count)

    return query
