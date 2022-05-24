from sqlalchemy import func

from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.artist_info2 import artist_info2_serializer


class GetArtistInfo2View(BaseView):
    def process_request(self, id_, count='20'):
        count = int(count)
        artist = Artist.query.get(id_)

        similar_artists = self.get_similar_artists(artist, count)

        return {
            'artistInfo2': artist_info2_serializer(artist, similar_artists)
        }

    @staticmethod
    def get_similar_artists(artist, count):
        genres_sq = Genre.query.with_entities(Genre.id_).distinct()
        genres_sq = genres_sq.join(Media.genres)
        genres_sq = genres_sq.filter(Media.artist == artist)

        artists_sq = Media.query.with_entities(Media.artist_id).distinct()
        artists_sq = artists_sq.join(Media.genres)
        artists_sq = artists_sq.filter(Genre.id_.in_(genres_sq))
        artists_sq = artists_sq.filter(Media.artist != artist)
        artists_sq = artists_sq.filter(Media.artist_id.isnot(None))

        if count:
            artists_sq = artists_sq.limit(count)

        artist_q = Artist.query.with_entities(
            Artist,
            func.count(Album.id_.distinct()).label('albums_count'),
        )
        artist_q = artist_q.join(Artist.albums)
        artist_q = artist_q.filter(Artist.id_.in_(artists_sq))
        artist_q = artist_q.group_by(Artist)

        return [{'artist': i[0], 'albums_count': i[1]} for i in artist_q]
