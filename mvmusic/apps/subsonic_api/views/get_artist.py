from sqlalchemy import func

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
        albums = Album.query.filter_by(artist=artist)
        albums_data = self.get_albums_data(artist)

        albums = [album_serializer(i, **albums_data[i.id_])
                  for i in albums.all()]

        media_image_id = list(albums_data.values())[0]['media_image_id']
        resp = artist_serializer(artist, len(albums), media_image_id)
        resp['album'] = sorted(albums, key=lambda i: (i['year'], i['name']))

        return {
            'artist': resp
        }

    # noinspection PyMethodMayBeStatic
    def get_albums_data(self, artist):
        query = Album.query.with_entities(
            Album.id_,
            func.count(Media.id_.distinct()),
            func.sum(Media.duration),
            func.min(Media.created_date),
            func.min(Media.year),
            func.string_agg(Genre.name.distinct(), ', '),
            func.min(Media.image_id)
        )

        query = query.join(Album.media)
        query = query.join(Media.genres)
        query = query.filter(Album.artist == artist)
        query = query.group_by(Album.id_)

        return {
            id_: {
                'songs_count': sc,
                'duration': dur,
                'created': cr,
                'year': year,
                'genres': genres,
                'media_image_id': image_id
            }
            for id_, sc, dur, cr, year, genres, image_id in query.all()
        }
