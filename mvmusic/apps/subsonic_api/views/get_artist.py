from sqlalchemy import func

from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.artist_with_albums_id3 import \
    artist_with_albums_id3_serializer


class GetArtistView(BaseView):
    def process_request(self, id_):
        artist = Artist.query.get(id_)
        albums_data = self.get_albums_data(artist)

        albums = []
        for album in artist.albums.all():
            album_data = albums_data[album.id_]
            album_data['album'] = album
            albums.append(album_data)

        return {
            'artist': artist_with_albums_id3_serializer(artist, albums)
        }

    @staticmethod
    def get_albums_data(artist):
        query = Album.query.with_entities(
            Album.id_,
            func.count(Media.id_.distinct()).label('songs_count'),
            func.sum(Media.duration).label('duration'),
            func.string_agg(Genre.name.distinct(), ', ').label('genres')
        )

        query = query.join(Album.media)
        query = query.join(Media.genres)
        query = query.filter(Album.artist == artist)
        query = query.group_by(Album.id_)

        return {i.id_: {k: i[k] for k in i.keys() if k != 'id_'}
                for i in query.all()}
