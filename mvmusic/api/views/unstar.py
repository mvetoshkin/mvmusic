from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.libs.database import session
from mvmusic.models.starred_album import StarredAlbum
from mvmusic.models.starred_artist import StarredArtist
from mvmusic.models.starred_directory import StarredDirectory
from mvmusic.models.starred_media import StarredMedia


@route("/unstar")
@auth_required
def unstar_view():
    entity_ids = request.values.getlist("id")
    album_ids = request.values.getlist("albumId")
    artist_ids = request.values.getlist("artistId")

    if entity_ids:
        for entity_id in entity_ids:
            try:
                query = select(StarredMedia).where(
                    StarredMedia.media_id == entity_id,
                    StarredMedia.user_id == g.current_user.id
                )
                item = session.scalars(query).one()
                session.delete(item)
                continue

            except NoResultFound:
                pass

            try:
                query = select(StarredDirectory).where(
                    StarredDirectory.directory_id == entity_id,
                    StarredDirectory.user_id == g.current_user.id
                )
                item = session.scalars(query).one()
                session.delete(item)

            except NoResultFound:
                pass

    if album_ids:
        for album_id in album_ids:
            try:
                query = select(StarredAlbum).where(
                    StarredAlbum.album_id == album_id,
                    StarredAlbum.user_id == g.current_user.id
                )
                item = session.scalars(query).one()
                session.delete(item)

            except NoResultFound:
                pass

    if artist_ids:
        for artist_id in artist_ids:
            try:
                query = select(StarredArtist).where(
                    StarredArtist.artist_id == artist_id,
                    StarredArtist.user_id == g.current_user.id
                )
                item = session.scalars(query).one()
                session.delete(item)

            except NoResultFound:
                pass

    return make_response()
