from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.directory import Directory
from mvmusic.models.media import Media
from mvmusic.models.starred_album import StarredAlbum
from mvmusic.models.starred_artist import StarredArtist
from mvmusic.models.starred_directory import StarredDirectory
from mvmusic.models.starred_media import StarredMedia


@route("/star")
@auth_required
def star_view():
    """Attaches a star to a song, album or artist."""

    entity_ids = request.values.getlist("id")
    album_ids = request.values.getlist("albumId")
    artist_ids = request.values.getlist("artistId")

    if entity_ids:
        for entity_id in entity_ids:
            try:
                star_media(entity_id)
                continue
            except NoResultFound:
                pass

            try:
                star_directory(entity_ids)
            except NoResultFound:
                pass

    if album_ids:
        for album_id in album_ids:
            star_album(album_id)

    if artist_ids:
        for artist_id in artist_ids:
            star_artist(artist_id)

    return make_response()


def star_media(media_id):
    query = select(Media).where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Media.id == media_id
    )

    media = session.scalars(query).one()

    try:
        query = select(StarredMedia).where(
            StarredMedia.media_id == media.id,
            StarredMedia.user_id == g.current_user.id
        )
        session.scalars(query).one()

    except NoResultFound:
        item = StarredMedia(media_id=media.id, user_id=g.current_user.id)
        session.add(item)


def star_directory(directory_id):
    query = select(Directory).where(
        Directory.library_id.in_([i.id for i in g.current_user.libraries]),
        Directory.id == directory_id
    )

    directory = session.scalars(query).unique().one()

    try:
        query = select(StarredDirectory).where(
            StarredDirectory.directory_id == directory.id,
            StarredDirectory.user_id == g.current_user.id
        )
        session.scalars(query).one()

    except NoResultFound:
        item = StarredDirectory(
            directory_id=directory.id,
            user_id=g.current_user.id
        )
        session.add(item)


def star_artist(artist_id):
    query = select(Artist).join(Artist.media).where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Artist.id == artist_id
    )

    artist = session.scalars(query).unique().one()

    try:
        query = select(StarredArtist).where(
            StarredArtist.artist_id == artist.id,
            StarredArtist.user_id == g.current_user.id
        )
        session.scalars(query).one()

    except NoResultFound:
        item = StarredArtist(artist_id=artist.id, user_id=g.current_user.id)
        session.add(item)


def star_album(album_id):
    query = select(Album).join(Album.media).where(
        Media.library_id.in_([i.id for i in g.current_user.libraries]),
        Album.id == album_id
    )

    album = session.scalars(query).unique().one()

    try:
        query = select(StarredAlbum).where(
            StarredAlbum.album_id == album.id,
            StarredAlbum.user_id == g.current_user.id
        )
        session.scalars(query).one()

    except NoResultFound:
        item = StarredAlbum(album_id=album.id, user_id=g.current_user.id)
        session.add(item)
