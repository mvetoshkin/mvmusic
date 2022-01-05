import logging
import os
from datetime import datetime
from uuid import uuid4

from dateutil import parser
from sqlalchemy.orm import noload

import mutagen
import mutagen.flac
import mutagen.mp3

from mvmusic.common.database import db
from mvmusic.common.exceptions import NotFoundError
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.directory import Directory
from mvmusic.models.genre import Genre
from mvmusic.models.image import Image
from mvmusic.models.library import Library
from mvmusic.models.media import Media
from mvmusic.settings import settings

logger = logging.getLogger(__name__)


def scan_libraries(ids=None):
    if not ids:
        ids = [i.id_ for i in Library.query.all()]

    for id_ in ids:
        scan_library(id_)


def scan_library(library_id):
    library = Library.query.get(library_id)
    scanner = Scanner(library)
    scanner.start()


class Scanner:
    library = None
    start_ts = None

    def __init__(self, library):
        self.library = library

    def start(self):
        logger.info(f'Scanning of the {self.library.name} library started')

        self.start_ts = datetime.utcnow()
        self.scan_directory(self.library.path)
        self.purge()
        db.session.commit()

        self.scan_media_data()
        # self.scan_artists()
        # self.scan_albums()

        logger.info(f'Scanning of the {self.library.name} library finished')

    def scan_directory(self, path, parent=None):
        item: os.DirEntry

        for item in os.scandir(path):
            lib_path_len = len(self.library.path)
            lib_path_len += 1  # include trailing /
            item_path = item.path[lib_path_len:]

            if item.is_dir():
                try:
                    directory = Directory.query.get_by(library=self.library,
                                                       path=item_path)
                    directory.last_seen = datetime.utcnow()
                except NotFoundError:
                    logger.info(f'Found new folder {item.path}')
                    directory = Directory.create(
                        path=item_path,
                        last_seen=datetime.utcnow(),
                        library=self.library,
                        parent=parent
                    )

                self.scan_directory(item.path, directory)

            else:
                try:
                    media = Media.query.get_by(library=self.library,
                                               path=item_path)
                    media.last_seen = datetime.utcnow()
                except NotFoundError:
                    logger.info(f'Found new media {item.path}')
                    Media.create(
                        path=item_path,
                        last_seen=datetime.utcnow(),
                        parent=parent,
                        library=self.library,
                    )

    def purge(self):
        for item in Media.query.filter(Media.last_seen < self.start_ts):
            item.delete()
            item_path = os.path.join(self.library.path, item.path)
            logger.info(f'Delete media {item_path}')

        for item in Directory.query.filter(Directory.last_seen < self.start_ts):
            item.delete()
            item_path = os.path.join(self.library.path, item.path)
            logger.info(f'Delete folder {item_path}')

        media_sq = Media.query.with_entities(Media.album_id).distinct()
        album_sq = Album.query.with_entities(Album.artist_id).distinct()
        artist_sq = Artist.query.with_entities(Artist.image_id).distinct()

        # Delete unused albums

        query = Album.query.options(noload('*')).filter(
            Album.id_.not_in(media_sq)
        )

        for item in query.all():
            item.delete()
            logger.info(f'Delete album {item.name}')

        # Delete unused artists

        query = Artist.query.options(noload('*')).filter(
            Artist.id_.not_in(album_sq),
            Artist.id_.not_in(media_sq)
        )

        for item in query.all():
            item.delete()
            logger.info(f'Delete artist {item.name}')

        # delete unused images

        images = Image.query.options(noload('*')).filter(
            Image.id_.not_in(artist_sq),
            Image.id_.not_in(album_sq),
            Image.id_.not_in(media_sq)
        )

        for image in images.all():
            image_path = os.path.join(settings.CACHE_PATH, image.path)
            if os.path.exists(image_path):
                os.remove(image_path)
            image.delete()
            logger.info(f'Delete image {image_path}')

    def scan_media_data(self):
        items = Media.query.filter(Media.title.is_(None))

        for item in items:
            self.scan_media_file(item)
            db.session.commit()

    def scan_media_file(self, media):
        media_path = os.path.join(media.library.path, media.path)
        logger.info(f'Scanning media {media_path}')

        media_file = mutagen.File(media_path)

        if type(media_file) == mutagen.flac.FLAC:
            self.parse_flac(media, media_file)
        if type(media_file) == mutagen.mp3.MP3:
            self.parse_mp3(media, media_file)

        media.bitrate = int(media_file.info.bitrate / 1000)
        media.duration = round(media_file.info.length)
        media.content_type = media_file.mime[0]
        media.size = os.stat(media_path).st_size
        media.is_video = False

    def parse_mp3(self, media, file):
        self.parse_tags(
            media,
            title=self.mp3_tag(file, 'TIT2'),
            release_date=self.mp3_tag(file, 'TDOR'),
            track=self.mp3_tag(file, 'TRCK'),
            artist_name=self.mp3_tag(file, 'TPE1'),
            album_name=self.mp3_tag(file, 'TALB'),
            mb_artist_id=self.mp3_tag(file, 'TXXX:MusicBrainz Artist Id'),
            mb_album_id=self.mp3_tag(file, 'TXXX:MusicBrainz Album Id'),
            image=self.mp3_tag(file, 'APIC:'),
            genres=self.mp3_tag(file, 'TCON')
        )

    def parse_flac(self, media, file):
        pictures = getattr(file, 'pictures')
        image = pictures[0].data if pictures else None

        self.parse_tags(
            media,
            title=self.flac_tag(file, 'TITLE'),
            release_date=self.flac_tag(file, 'ORIGINALDATE'),
            track=self.flac_tag(file, 'TRACKNUMBER'),
            artist_name=self.flac_tag(file, 'ARTIST'),
            album_name=self.flac_tag(file, 'ALBUM'),
            mb_artist_id=self.flac_tag(file, 'MUSICBRAINZ_ARTISTID'),
            mb_album_id=self.flac_tag(file, 'MUSICBRAINZ_ALBUMID'),
            image=image,
            genres=file.tags.get('GENRE')
        )

    @staticmethod
    def mp3_tag(file, tag_name):
        tag = file.tags.get(tag_name)
        if not tag:
            return None

        if tag_name == 'APIC:':
            return tag.data

        if tag_name == 'TCON':
            return tag.genres

        text = tag.text[0]
        if not text:
            return None

        if tag_name == 'TDOR':
            return text.year

        return text.strip()

    @staticmethod
    def flac_tag(file, tag_name):
        tag = file.tags.get(tag_name)
        if not tag:
            return None

        if tag_name == 'ORIGINALDATE':
            return parser.parse(tag[0]).year

        return tag[0].strip()

    def parse_tags(self, media, title, release_date, track, artist_name,
                   album_name, mb_artist_id, mb_album_id, image, genres):
        genres = genres or []

        media.title = title
        media.year = release_date
        media.track = self.get_track(track)

        media.artist = self.get_artist(artist_name, mb_artist_id)
        media.album = self.get_album(media.artist, album_name, mb_album_id)

        if not self.is_image_same(media, image):
            media.image = self.save_image(image)

        new_genres = set()
        for genre_name in genres:
            genre = self.get_genre(genre_name)
            new_genres.add(genre.id_)
            if genre not in media.genres:
                media.genres.append(genre)

        for genre in media.genres:
            if genre.id_ not in new_genres:
                media.genres.remove(genre)

    @staticmethod
    def get_track(track):
        if not track:
            return None
        return track.split('/')[0] if type(track) is str else track

    @staticmethod
    def get_artist(name, music_brainz_id):
        if not name:
            name = '[unknown]'

        try:
            artist = Artist.query.get_by(name=name)
        except NotFoundError:
            artist = Artist.create(name=name)

        if music_brainz_id and artist.music_brainz_id != music_brainz_id:
            artist.music_brainz_id = music_brainz_id

        return artist

    @staticmethod
    def get_album(artist, name, music_brainz_id):
        if not name:
            name = '[non-album tracks]'

        try:
            album = Album.query.get_by(artist=artist, name=name)
        except NotFoundError:
            album = Album.create(name=name, artist=artist)

        if music_brainz_id and album.music_brainz_id != music_brainz_id:
            album.music_brainz_id = music_brainz_id

        return album

    @staticmethod
    def get_genre(genre_name):
        genre_name = genre_name.strip()

        try:
            return Genre.query.get_by(name=genre_name)
        except NotFoundError:
            return Genre.create(name=genre_name)

    @staticmethod
    def save_image(image):
        if not image:
            return None

        id_ = str(uuid4())
        image_cache_path = os.path.join('images', id_[:2], id_[2:4], id_)
        image_path = os.path.join(settings.CACHE_PATH, image_cache_path)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with open(image_path, 'wb') as file:
            file.write(image)

        return Image(id_=id_, path=image_cache_path)

    @staticmethod
    def is_image_same(obj, image):
        if obj.image is None and image is None:
            return True

        if bool(obj.image is None) != bool(image is None):
            return False

        file_path = os.path.join(settings.CACHE_PATH, obj.image.path)
        with open(file_path, 'rb') as file:
            media_image = file.read()

        return media_image == image

    def scan_artists(self):
        items = Artist.query.filter(Artist.notes.is_(None))

        for item in items:
            self.scan_artist(item)
            db.session.commit()

    @staticmethod
    def scan_artist(artist):
        pass

    def scan_albums(self):
        items = Album.query.filter(Album.notes.is_(None))

        for item in items:
            self.scan_album(item)
            db.session.commit()

    @staticmethod
    def scan_album(album):
        pass
