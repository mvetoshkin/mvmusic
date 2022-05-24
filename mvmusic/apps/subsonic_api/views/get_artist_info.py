from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.artist_info import artist_info_serializer


class GetArtistInfoView(BaseView):
    def process_request(self, id_, count='20'):
        count = int(count)
        artist = Artist.query.get(id_)

        similar_artists = self.get_similar_artists(artist, count)

        return {
            'artistInfo': artist_info_serializer(artist, similar_artists)
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

        return Artist.query.filter(Artist.id_.in_(artists_sq))
