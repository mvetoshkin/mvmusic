from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import BadRequest, Forbidden

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.songs import songs_serializer
from mvmusic.libs.database import session
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media
from mvmusic.models.media_genre import MediaGenre


@route("/getSongsByGenre")
@auth_required
def get_songs_by_genre_view():
    genre = request.values["genre"]
    offset = int(request.values.get("offset", "0"))
    music_folder_id = request.values.get("musicFolderId")

    count = int(request.values.get("count", "10"))
    count = max(count, 1)
    count = min(count, 500)

    library_ids = [i.id for i in g.current_user.libraries]

    if music_folder_id:
        if music_folder_id not in library_ids:
            raise Forbidden
        library_ids = [music_folder_id]

    try:
        query = select(Genre).where(
            func.lower(Genre.name) == func.lower(genre)  # type: ignore
        )
        genre_obj = session.scalars(query).one()
    except NoResultFound:
        raise BadRequest("Genre not found")

    query = select(Media).join(MediaGenre)
    query = query.where(
        MediaGenre.genre_id == genre_obj.id,
        Media.library_id.in_(library_ids)
    )

    query = query.order_by(Media.created_at)
    query = query.limit(count)
    query = query.offset(count * offset)

    songs = session.scalars(query).unique()

    data = songs_serializer(songs)
    return make_response({"songsByGenre": data})
