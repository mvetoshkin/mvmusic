from flask import g
from sqlalchemy import func, select

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.genres import genres_serializer
from mvmusic.libs.database import session
from mvmusic.models.genre import Genre
from mvmusic.models.media import Media


@route("/getGenres")
@auth_required
def get_genres_view():
    library_ids = [i.id for i in g.current_user.libraries]

    genres = []
    genres_data = get_genres_data(library_ids)

    query = select(Genre).distinct()
    query = query.outerjoin(Genre.media)
    query = query.where(Media.library_id.in_(library_ids))
    query = query.order_by(Genre.name)

    for genre in session.scalars(query):
        data = genres_data[genre.id]
        data["genre"] = genre
        genres.append(data)

    data = genres_serializer(genres)
    return make_response({"genres": data})


def get_genres_data(library_ids):
    query = select(
        Genre.id,
        func.count(Media.id.distinct()).label("songs_count"),
        func.count(Media.album_id.distinct()).label("albums_count")
    )

    query = query.outerjoin(Genre.media)
    query = query.where(Media.library_id.in_(library_ids))
    query = query.group_by(Genre.id)

    items = {}

    for i in session.execute(query):
        items[i.id] = {
            "songs_count": i.songs_count,
            "albums_count": i.albums_count
        }

    return items
