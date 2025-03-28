from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import BadRequest, NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.songs import songs_serializer
from mvmusic.libs.database import session
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media


@route("/getRandomSongs")
@auth_required
def get_random_songs_view():
    """Returns random songs matching the given criteria."""

    size = int(request.values.get("size", "10"))
    size = max(size, 1)
    size = min(size, 500)

    genre = request.values.get("genre")
    from_year = request.values.get("fromYear")
    to_year = request.values.get("toYear")
    music_folder_id = request.values.get("musicFolderId")

    library_ids = [i.id for i in g.current_user.libraries]

    if music_folder_id:
        if music_folder_id not in library_ids:
            raise NotFound
        library_ids = [music_folder_id]

    query = select(Media).options(
        joinedload(Media.artist),
        joinedload(Media.album),
        joinedload(Media.genres)
    )
    query = query.order_by(func.random())
    query = query.where(Media.library_id.in_(library_ids))

    if genre:
        try:
            genre_query = select(Genre).where(Genre.name.ilike(genre))
            genre_obj = session.scalars(genre_query).one()
        except NoResultFound:
            raise BadRequest("Genre not found")

        query = query.join(Media.genres)
        query = query.where(Genre.id == genre_obj.id)

    if from_year:
        query = query.where(Media.year >= int(from_year))

    if to_year:
        query = query.where(Media.year <= int(to_year))

    if size:
        query = query.limit(size)

    songs = session.scalars(query).unique()

    data = songs_serializer(songs)
    return make_response({"randomSongs": data})
