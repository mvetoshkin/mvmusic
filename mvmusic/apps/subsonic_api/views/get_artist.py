from sqlalchemy import func
from sqlalchemy.orm import noload

from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from . import BaseView
from ..serializers.album import album_serializer
from ..serializers.artist import artist_serializer


class GetArtistView(BaseView):
    def process_request(self, id_):
        artist = Artist.query.get(id_)

        year_field = func.min(Media.year)

        query = Album.query.with_entities(
            Album,
            func.count(Media.id_.distinct()),
            func.sum(Media.duration),
            func.min(Media.created_date),
            year_field,
            func.string_agg(Genre.name.distinct(), ', '),
            func.min(Media.image_id)
        )

        query = query.options(noload(Album.artist))
        query = query.join(Album.media)
        query = query.join(Media.genres)
        query = query.filter(Album.artist == artist)
        query = query.group_by(Album)
        query = query.order_by(year_field.asc(), Album.name)

        albums = [
            album_serializer(album, sc, dur, cr, year, genres, media_image_id)
            for album, sc, dur, cr, year, genres, media_image_id in query.all()
        ]

        resp = artist_serializer(artist, len(albums))
        resp['album'] = albums

        return {
            'artist': resp
        }
