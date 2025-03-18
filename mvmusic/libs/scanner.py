import logging
import os
import time
from pathlib import Path
from uuid import uuid4

import mutagen
import mutagen.flac
import mutagen.mp3
from dateutil import parser
from PIL import Image as PILImage
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import noload

from mvmusic.libs import get_request, utcnow
from mvmusic.libs.database import session
from mvmusic.libs.discogs import get_discogs_album, get_discogs_artist, \
    search_discogs_album, search_discogs_artist
from mvmusic.libs.musicbrainz import get_mb_album, get_mb_artist
from mvmusic.libs.wiki import parse_wiki, parse_wikidata
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.directory import Directory
from mvmusic.models.genre import Genre
from mvmusic.models.image import Image
from mvmusic.models.library import Library
from mvmusic.models.media import Media
from mvmusic.settings import MEDIA_PATH

IMAGES_DIR = Path("images")
logger = logging.getLogger(__name__)


def scan_libraries(ids=None, full=False):
    if not ids:
        query = select(Library)
        ids = [i.id for i in session.scalars(query)]

    for lib_id in ids:
        scan_library(lib_id, full)


def scan_library(library_id, full=False):
    library = session.get(Library, library_id)

    logger.info(f"Scanning of the {library.name} library started")

    start_ts = utcnow()

    scan_directory(library, library.path)
    session.commit()

    scan_media_data(full)
    session.commit()

    scan_artists(full)
    scan_albums(full)
    session.commit()

    purge(library, start_ts)

    logger.info(f"Scanning of the {library.name} library finished")


def scan_directory(library, path, parent_dir=None):
    for item in os.scandir(path):
        lib_path_len = len(library.path)
        lib_path_len += 1  # include trailing /
        item_path = item.path[lib_path_len:]

        if item.is_dir():
            try:
                query = select(Directory).where(
                    Directory.library == library,
                    Directory.path == item_path
                )

                directory = session.scalars(query).one()
                directory.last_seen = utcnow()

            except NoResultFound:
                logger.info(f"Found new folder {item.path}")

                directory = Directory()
                directory.path = item_path
                directory.last_seen = utcnow()
                directory.library = library
                directory.parent = parent_dir

                session.add(directory)

            scan_directory(library, item.path, directory)

        else:
            try:
                query = select(Media).where(
                    Media.library == library,
                    Media.path == item_path
                )

                media = session.scalars(query).unique().one()
                media.last_seen = utcnow()

            except NoResultFound:
                logger.info(f"Found new media {item.path}")

                media = Media(
                    path=item_path,
                    last_seen=utcnow(),
                    parent_id=parent_dir.id,
                    library_id=library.id
                )

                session.add(media)


def scan_media_data(full=False):
    query = select(Media)

    if not full:
        query = query.where(Media.scanned == False)

    for item in session.scalars(query).unique():
        scan_media_file(item)
        set_parent_image(item)
        item.scanned = True


def scan_media_file(media):
    media_path = Path(media.library.path) / media.path
    logger.info(f"Scanning media {media_path}")

    media_file = mutagen.File(media_path)

    if type(media_file) == mutagen.flac.FLAC:
        parse_flac(media, media_file)
    if type(media_file) == mutagen.mp3.MP3:
        parse_mp3(media, media_file)

    media.bitrate = int(media_file.info.bitrate / 1000)
    media.duration = round(media_file.info.length)
    media.content_type = media_file.mime[0]
    media.size = os.stat(media_path).st_size
    media.is_video = False


def parse_flac(media, file):
    pictures = getattr(file, "pictures")
    image = pictures[0].data if pictures else None

    artist_name = flac_tag(file, "ALBUMARTIST") or \
                  flac_tag(file, "ARTIST")

    parse_tags(
        media,
        title=flac_tag(file, "TITLE"),
        release_date=flac_tag(file, "ORIGINALDATE"),
        track=flac_tag(file, "TRACKNUMBER"),
        disc_number=flac_tag(file, "DISCNUMBER"),
        artist_name=artist_name,
        album_name=flac_tag(file, "ALBUM"),
        mb_artist_id=flac_tag(file, "MUSICBRAINZ_ARTISTID"),
        mb_album_id=flac_tag(file, "MUSICBRAINZ_ALBUMID"),
        image=image,
        genres=file.tags.get("GENRE")
    )


def flac_tag(file, tag_name):
    tag = file.tags.get(tag_name)
    if not tag:
        return None

    if tag_name == "ORIGINALDATE":
        return parser.parse(tag[0]).year

    return tag[0].strip()


def parse_mp3(media, file):
    artist_name = mp3_tag(file, "TPE2") or \
                  mp3_tag(file, "TPE1")

    disc, track = get_disc_and_track(mp3_tag(file, "TRCK"))

    parse_tags(
        media,
        title=mp3_tag(file, "TIT2"),
        release_date=mp3_tag(file, "TDOR"),
        track=track,
        disc_number=disc,
        artist_name=artist_name,
        album_name=mp3_tag(file, "TALB"),
        mb_artist_id=mp3_tag(file, "TXXX:MusicBrainz Artist Id"),
        mb_album_id=mp3_tag(file, "TXXX:MusicBrainz Album Id"),
        image=mp3_tag(file, "APIC:"),
        genres=mp3_tag(file, "TCON")
    )


def get_disc_and_track(track):
    if not track:
        return None, None

    if "/" not in track:
        return None, track

    return track.split("/") if type(track) is str else (1, track)


def mp3_tag(file, tag_name):
    tag = file.tags.get(tag_name)
    if not tag:
        return None

    if tag_name == "APIC:":
        return tag.data

    if tag_name == "TCON":
        return tag.genres

    text = tag.text[0]
    if not text:
        return None

    if tag_name == "TDOR":
        return text.year

    return text.strip()


def parse_tags(media, title, release_date, track, disc_number,
               artist_name, album_name, mb_artist_id, mb_album_id, image,
               genres):
    genres = genres or []

    media.title = title
    media.year = release_date
    media.track = track
    media.disc_number = disc_number

    if not is_image_same(media, image):
        media.image = save_image(image)

    media.artist = get_artist(artist_name)
    if mb_artist_id and media.artist.music_brainz_id != mb_artist_id:
        media.artist.music_brainz_id = mb_artist_id
    if media.image and not media.artist.image:
        media.artist.image = media.image

    media.album = get_album(media.artist, album_name, media.year)
    if mb_album_id and media.album.music_brainz_id != mb_album_id:
        media.album.music_brainz_id = mb_album_id
    if media.year and not media.album.year:
        media.album.year = media.year
    if media.image and not media.album.image:
        media.album.image = media.image

    new_genres = set()
    for genre_name in genres:
        genre = get_genre(genre_name)
        new_genres.add(genre.id)
        if genre not in media.genres:
            media.genres.append(genre)

    for genre in media.genres:
        if genre.id not in new_genres:
            media.genres.remove(genre)


def is_image_same(obj, image):
    if obj.image is None and image is None:
        return True

    if bool(obj.image is None) != bool(image is None):
        return False

    file_path = MEDIA_PATH / obj.image.path
    with open(file_path, "rb") as file:
        media_image = file.read()

    return media_image == image


def save_image(image):
    if not image:
        return None

    img_id = str(uuid4())
    img_path = IMAGES_DIR / img_id
    file_path = MEDIA_PATH / img_path

    os.makedirs(file_path.parent, exist_ok=True)

    with open(file_path, "wb") as file:
        file.write(image)

    with PILImage.open(file_path) as img:
        mimetype = PILImage.MIME[img.format]
        height = img.height
        width = img.width

    image = Image(
        id=img_id,
        path=str(img_path),
        mimetype=mimetype,
        height=height,
        width=width
    )

    session.add(image)

    return image


def get_artist(name):
    if not name:
        name = "[unknown]"

    try:
        query = select(Artist).where(Artist.name == name)
        artist = session.scalars(query).one()
    except NoResultFound:
        artist = Artist(name=name)
        session.add(artist)

    return artist


def get_album(artist, name, year):
    if not name:
        name = "[non-album tracks]"

    try:
        query = select(Album).where(
            Album.artist_id == artist.id,
            Album.name == name,
            Album.year == year
        )
        album = session.scalars(query).one()

    except NoResultFound:
        album = Album(name=name, year=year, artist_id=artist.id)
        session.add(album)

    return album


def get_genre(genre_name):
    genre_name = genre_name.strip()

    try:
        query = select(Genre).where(Genre.name == genre_name)
        return session.scalars(query).one()
    except NoResultFound:
        genre = Genre(name=genre_name)
        session.add(genre)
        return genre


def set_parent_image(obj):
    if obj.parent and obj.parent.image != obj.image:
        obj.parent.image = obj.image
        set_parent_image(obj.parent)


def scan_artists(full=False):
    query = select(Artist)

    if not full:
        query = query.where(Artist.scanned == False)

    for item in session.scalars(query):
        scan_artist(item)
        item.scanned = True
        time.sleep(1)


def scan_artist(artist):
    if artist.music_brainz_id:
        artist_info = get_mb_artist(artist)

        if artist_info.get("discogs_id"):
            discogs_info = get_discogs_artist(artist_info["discogs_id"])
            artist_info.update({k: v for k, v in discogs_info.items()
                                if not artist_info.get(k)})
    else:
        artist_info = search_discogs_artist(artist)

    if not artist_info:
        return

    if artist_info.get("wikidata_url"):
        artist_info.update(parse_wikidata(artist_info["wikidata_url"]))
    elif artist_info.get("wiki_url"):
        artist_info.update(parse_wiki(artist_info["wiki_url"]))

    artist.last_fm_url = artist_info.get("last_fm_url")
    artist.notes = artist_info.get("notes")

    if artist_info.get("image_url"):
        image_url = artist_info["image_url"]
        resp = get_request(image_url)

        if resp.status_code != 200:
            logger.error(f"Failed to get image {image_url}")
            return

        if not is_image_same(artist, resp.content):
            artist.image = save_image(resp.content)


def scan_albums(full):
    query = select(Album)

    if not full:
        query = query.where(Album.scanned == False)

    for item in session.scalars(query).unique():
        scan_album(item)
        item.scanned = True
        time.sleep(1)

def scan_album(album):
    if album.music_brainz_id:
        album_info = get_mb_album(album)

        if album_info.get("discogs_id"):
            discogs_info = get_discogs_album(album_info["discogs_id"])
            album_info.update({k: v for k, v in discogs_info.items()
                               if not album_info.get(k)})
    else:
        album_info = search_discogs_album(album)

    if not album_info:
        return

    if album_info.get("wikidata_url"):
        album_info.update(parse_wikidata(album_info["wikidata_url"]))
    elif album_info.get("wiki_url"):
        album_info.update(parse_wiki(album_info["wiki_url"]))

    album.last_fm_url = album_info.get("last_fm_url")
    album.notes = album_info.get("notes")

    if album_info.get("image_url"):
        image_url = album_info["image_url"]
        resp = get_request(image_url)

        if resp.status_code != 200:
            logger.error(f"Failed to get image {image_url}")
            return

        if not is_image_same(album, resp.content):
            album.image = save_image(resp.content)


def purge(library, start_ts):
    query = select(Media).where(Media.last_seen < start_ts)
    for item in session.scalars(query).unique():
        session.delete(item)
        item_path = Path(library.path) / item.path
        logger.info(f"Delete media {item_path}")

    query = select(Directory).where(Directory.last_seen < start_ts)
    for item in session.scalars(query):
        session.delete(item)
        item_path = Path(library.path) / item.path
        logger.info(f"Delete folder {item_path}")

    # Delete unused albums

    media_q = select(Media.album_id).distinct().where(Media.album_id != None)

    query = select(Album).options(noload("*"))  # type: ignore
    query = query.where(Album.id.not_in(media_q))

    for item in session.scalars(query):
        session.delete(item)
        logger.info(f"Delete album {item.name}")

    # Delete unused artists

    album_q = select(Album.artist_id).distinct().where(Album.artist_id != None)
    media_q = select(Media.artist_id).distinct().where(Media.artist_id != None)

    query = select(Artist).options(noload("*"))  # type: ignore
    query = query.where(
        Artist.id.not_in(album_q),
        Artist.id.not_in(media_q)
    )

    for item in session.scalars(query):
        session.delete(item)
        logger.info(f"Delete artist {item.name}")

    # delete unused images

    artist_q = select(Artist.image_id).distinct().where(Artist.image_id != None)
    album_q = select(Album.image_id).distinct().where(Album.image_id != None)
    media_q = select(Media.image_id).distinct().where(Media.image_id != None)
    directory_q = select(Directory.image_id).distinct().where(
        Directory.image_id != None
    )

    query = select(Image).options(noload("*"))  # type: ignore
    query = query.where(
        Image.id.not_in(artist_q),
        Image.id.not_in(album_q),
        Image.id.not_in(media_q),
        Image.id.not_in(directory_q),
    )

    for image in session.scalars(query):
        file_path = MEDIA_PATH / image.path
        if file_path.exists():
            os.remove(file_path)
        session.delete(image)
        logger.info(f"Delete image {file_path}")
