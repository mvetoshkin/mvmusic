import logging
import os
import shutil
import time
from datetime import datetime
from uuid import uuid4

import mutagen
import mutagen.flac
import mutagen.mp3
import requests
from dateutil import parser
from PIL import Image as PILImage
from sqlalchemy.orm import noload

from mvmusic.libs.database import db
from mvmusic.libs.discogs import get_discogs_album, get_discogs_artist, \
    search_discogs_album, search_discogs_artist
from mvmusic.libs.exceptions import NotFoundError
from mvmusic.libs.musicbrainz import get_mb_album, get_mb_artist
from mvmusic.libs.wiki import parse_wiki, parse_wikidata
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.directory import Directory
from mvmusic.models.genre import Genre
from mvmusic.models.image import Image
from mvmusic.models.library import Library
from mvmusic.models.media import Media
from mvmusic.settings import settings

logger = logging.getLogger(__name__)


def scan_libraries(ids=None, full=False):
    if not ids:
        ids = [i.id_ for i in Library.query.all()]

    for id_ in ids:
        scan_library(id_, full)


def scan_library(library_id, full=False):
    library = Library.query.get(library_id)
    scanner = Scanner(library)
    scanner.start(full)


class Scanner:
    library = None
    start_ts = None

    def __init__(self, library):
        self.library = library

    def start(self, full=False):
        logger.info(f'Scanning of the {self.library.name} library started')

        self.start_ts = datetime.utcnow()
        self.scan_directory(self.library.path)
        db.session.commit()

        self.scan_media_data(full)
        self.scan_artists(full)
        self.scan_albums(full)

        self.purge()

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
        query = Media.query.filter(Media.last_seen < self.start_ts)
        for item in query.all():
            item.delete()
            item_path = os.path.join(self.library.path, item.path)
            logger.info(f'Delete media {item_path}')

        query = Directory.query.filter(Directory.last_seen < self.start_ts)
        for item in query.all():
            item.delete()
            item_path = os.path.join(self.library.path, item.path)
            logger.info(f'Delete folder {item_path}')

        media_sq = Media.query.with_entities(Media.album_id).distinct()
        media_sq = media_sq.filter(Media.album_id.isnot(None))
        album_sq = Album.query.with_entities(Album.artist_id).distinct()
        album_sq = album_sq.filter(Album.artist_id.isnot(None))
        artist_sq = Artist.query.with_entities(Artist.image_id).distinct()
        artist_sq = artist_sq.filter(Artist.image_id.isnot(None))

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

        query = Image.query.options(noload('*')).filter(
            Image.id_.not_in(artist_sq),
            Image.id_.not_in(album_sq),
            Image.id_.not_in(media_sq)
        )

        for image in query.all():
            image_path = os.path.join(settings.CACHE_PATH, image.path)
            image_dir = os.path.dirname(image_path)
            if os.path.exists(image_dir):
                shutil.rmtree(image_dir)
            image.delete()
            logger.info(f'Delete image {image_dir}')

    def scan_media_data(self, full=False):
        query = Media.query

        if not full:
            query = query.filter(Media.title.is_(None))

        for item in query.all():
            self.scan_media_file(item)
            self.set_parent_image(item)
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
        artist_name = self.mp3_tag(file, 'TPE2') or \
            self.mp3_tag(file, 'TPE1')

        disc, track = self.get_disc_and_track(self.mp3_tag(file, 'TRCK'))

        self.parse_tags(
            media,
            title=self.mp3_tag(file, 'TIT2'),
            release_date=self.mp3_tag(file, 'TDOR'),
            track=track,
            disc_number=disc,
            artist_name=artist_name,
            album_name=self.mp3_tag(file, 'TALB'),
            mb_artist_id=self.mp3_tag(file, 'TXXX:MusicBrainz Artist Id'),
            mb_album_id=self.mp3_tag(file, 'TXXX:MusicBrainz Album Id'),
            image=self.mp3_tag(file, 'APIC:'),
            genres=self.mp3_tag(file, 'TCON')
        )

    def parse_flac(self, media, file):
        pictures = getattr(file, 'pictures')
        image = pictures[0].data if pictures else None

        artist_name = self.flac_tag(file, 'ALBUMARTIST') or \
            self.flac_tag(file, 'ARTIST')

        self.parse_tags(
            media,
            title=self.flac_tag(file, 'TITLE'),
            release_date=self.flac_tag(file, 'ORIGINALDATE'),
            track=self.flac_tag(file, 'TRACKNUMBER'),
            disc_number=self.flac_tag(file, 'DISCNUMBER'),
            artist_name=artist_name,
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

    def parse_tags(self, media, title, release_date, track, disc_number,
                   artist_name, album_name, mb_artist_id, mb_album_id, image,
                   genres):
        genres = genres or []

        media.title = title
        media.year = release_date
        media.track = track
        media.disc_number = disc_number

        if not self.is_image_same(media, image):
            media.image = self.save_image(image)

        media.artist = self.get_artist(artist_name)
        if mb_artist_id and media.artist.music_brainz_id != mb_artist_id:
            media.artist.music_brainz_id = mb_artist_id
        if media.image and not media.artist.image:
            media.artist.image = media.image

        media.album = self.get_album(media.artist, album_name, media.year)
        if mb_album_id and media.album.music_brainz_id != mb_album_id:
            media.album.music_brainz_id = mb_album_id
        if media.year and not media.album.year:
            media.album.year = media.year
        if media.image and not media.album.image:
            media.album.image = media.image

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
    def get_disc_and_track(track):
        if not track:
            return None, None

        if '/' not in track:
            return None, track

        return track.split('/') if type(track) is str else (1, track)

    @staticmethod
    def get_artist(name):
        if not name:
            name = '[unknown]'

        try:
            artist = Artist.query.get_by(name=name)
        except NotFoundError:
            artist = Artist.create(name=name)

        return artist

    @staticmethod
    def get_album(artist, name, year):
        if not name:
            name = '[non-album tracks]'

        try:
            album = Album.query.get_by(artist=artist, name=name, year=year)
        except NotFoundError:
            album = Album.create(name=name, year=year, artist=artist)

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
        img_cache_path = os.path.join('images', id_[:2], id_[2:4], id_, 'orig')
        img_path = os.path.join(settings.CACHE_PATH, img_cache_path)

        os.makedirs(os.path.dirname(img_path), exist_ok=True)

        with open(img_path, 'wb') as file:
            file.write(image)

        with PILImage.open(img_path) as img:
            mimetype = PILImage.MIME[img.format]
            height = img.height
            width = img.width

        return Image(id_=id_, path=img_cache_path, mimetype=mimetype,
                     height=height, width=width)

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

    def set_parent_image(self, obj):
        if obj.parent and obj.parent.image != obj.image:
            obj.parent.image = obj.image
            self.set_parent_image(obj.parent)

    def scan_artists(self, full=False):
        query = Artist.query

        if not full:
            query = query.filter(Artist.notes.is_(None))

        for item in query.all():
            self.scan_artist(item)
            db.session.commit()
            time.sleep(1)

    def scan_artist(self, artist):
        if artist.music_brainz_id:
            artist_info = get_mb_artist(artist)

            if artist_info.get('discogs_id'):
                discogs_info = get_discogs_artist(artist_info['discogs_id'])
                artist_info.update({k: v for k, v in discogs_info.items()
                                   if not artist_info.get(k)})
        else:
            artist_info = search_discogs_artist(artist)

        if not artist_info:
            return

        if artist_info.get('wikidata_url'):
            artist_info.update(parse_wikidata(artist_info['wikidata_url']))
        elif artist_info.get('wiki_url'):
            artist_info.update(parse_wiki(artist_info['wiki_url']))

        artist.last_fm_url = artist_info.get('last_fm_url')
        artist.notes = artist_info.get('notes')

        if artist_info.get('image_url'):
            resp = requests.get(artist_info['image_url'])
            if not self.is_image_same(artist, resp.content):
                artist.image = self.save_image(resp.content)

    def scan_albums(self, full):
        query = Album.query

        if not full:
            query = query.filter(Album.notes.is_(None))

        for item in query.all():
            self.scan_album(item)
            db.session.commit()
            time.sleep(1)

    def scan_album(self, album):
        if album.music_brainz_id:
            album_info = get_mb_album(album)

            if album_info.get('discogs_id'):
                discogs_info = get_discogs_album(album_info['discogs_id'])
                album_info.update({k: v for k, v in discogs_info.items()
                                   if not album_info.get(k)})
        else:
            album_info = search_discogs_album(album)

        if not album_info:
            return

        if album_info.get('wikidata_url'):
            album_info.update(parse_wikidata(album_info['wikidata_url']))
        elif album_info.get('wiki_url'):
            album_info.update(parse_wiki(album_info['wiki_url']))

        album.last_fm_url = album_info.get('last_fm_url')
        album.notes = album_info.get('notes')

        if album_info.get('image_url'):
            resp = requests.get(album_info['image_url'])
            if not self.is_image_same(album, resp.content):
                album.image = self.save_image(resp.content)
