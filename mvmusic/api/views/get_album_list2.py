from flask import g, request
from sqlalchemy import func, nullslast, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import BadRequest, NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.album_list2 import album_list2_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.genre import Genre
from mvmusic.models.history import History
from mvmusic.models.media import Media
from mvmusic.models.starred_album import StarredAlbum


@route("/getAlbumList2")
@auth_required
def get_album_list2_view():
    """Similar to getAlbumList, but organizes music according to ID3 tags."""

    list_type = request.values["type"]

    size = int(request.values.get("size", "10"))
    size = max(size, 1)
    size = min(size, 500)

    offset = int(request.values.get("offset", "0"))

    music_folder_id = request.values.get("musicFolderId")
    library_ids = [i.id for i in g.current_user.libraries]
    if music_folder_id:
        if music_folder_id not in library_ids:
            raise NotFound
        library_ids = [music_folder_id]

    if list_type == "random":
        subq = select(Album.id).distinct()
        subq = subq.join(Album.media)
        subq = subq.where(Media.library_id.in_(library_ids))

        query = select(Album).options(joinedload(Album.artist))
        query = query.where(Album.id.in_(subq))
        query = query.order_by(func.random())
        query = query.limit(size)
        query = query.offset(size * offset)

        albums = [i for i in session.scalars(query).unique()]
        albums = get_albums_data(albums)

        data = album_list2_serializer(albums)
        return make_response({"albumList2": data})

    if list_type == "newest":
        query = select(Album).distinct()
        query = query.where(Album.year != None)
        query = query.order_by(Album.year.desc(), Album.name)

    elif list_type == "frequent":
        stats_sq = select(History.media_id, func.sum(1).label("plays_count"))
        stats_sq = stats_sq.where(History.user_id == g.current_user.id)
        stats_sq = stats_sq.group_by(History.media_id)
        stats_sq = stats_sq.subquery()

        query = select(Album, stats_sq.c.plays_count).distinct()
        query = query.outerjoin(stats_sq)
        query = query.order_by(
            nullslast(stats_sq.c.plays_count.desc()),
            Album.name
        )

    elif list_type == "recent":
        stats_sq = select(History.media_id,
                          func.max(History.modified_at).label("played_at"))
        stats_sq = stats_sq.where(History.user_id == g.current_user.id)
        stats_sq = stats_sq.group_by(History.media_id)
        stats_sq = stats_sq.subquery()

        query = select(Album, stats_sq.c.played_at).distinct()
        query = query.join(Album.media)
        query = query.outerjoin(stats_sq)
        query = query.order_by(
            nullslast(stats_sq.c.played_at.desc()),
            Album.name
        )

    elif list_type == "starred":
        query = select(Album).distinct()
        query = query.join(StarredAlbum)
        query = query.where(StarredAlbum.user_id == g.current_user.id)
        query = query.order_by(Album.name)

    elif list_type == "alphabeticalByName":
        query = select(Album.name).distinct()
        query = query.order_by(Album.name)

    elif list_type == "alphabeticalByArtist":
        query = select(Album, Artist.name).distinct()
        query = query.order_by(Artist.name, Album.name)

    elif list_type == "byYear":
        from_year = request.values["fromYear"]
        to_year = request.values["toYear"]

        query = select(Album.year).distinct()
        query = query.where(Album.year != None)

        reverse = False

        if from_year > to_year:
            reverse = True
            from_year, to_year = to_year, from_year

        query = query.where(
            Album.year >= int(from_year),
            Album.year <= int(to_year)
        )

        query = query.order_by(
            Album.year.desc() if reverse else Album.year,
            Album.name
        )

    elif list_type == "byGenre":
        genre = request.values["genre"]

        try:
            genre_query = select(Genre).where(Genre.name.ilike(genre))
            genre_obj = session.scalars(genre_query).one()
        except NoResultFound:
            raise BadRequest("Genre not found")

        query = select(Album).distinct()
        query = query.join(Album.media)
        query = query.join(Media.genres)
        query = query.where(Genre.id == genre_obj.id)
        query = query.order_by(Album.name)

    else:
        raise BadRequest("Unsupported list type")

    query = query.options(joinedload(Album.artist))
    query = query.join(Album.media)
    query = query.where(Media.library_id.in_(library_ids))
    query = query.limit(size)
    query = query.offset(size * offset)

    albums = [i[0] for i in session.execute(query)]
    albums = get_albums_data(albums)

    data = album_list2_serializer(albums)
    return make_response({"albumList2": data})


def get_albums_data(albums):
    query = select(
        Album.id,
        func.count(Media.id.distinct()).label("songs_count"),
        func.sum(Media.duration).label("duration"),
        func.string_agg(Genre.name.distinct(), ", ").label("genres")
    )

    query = query.join(Album.media)
    query = query.outerjoin(Media.genres)
    query = query.where(Album.id.in_({i.id for i in albums}))
    query = query.group_by(Album.id)

    albums_data = {}

    for i in session.execute(query):
        albums_data[i.id] = {
            "songs_count": i.songs_count,
            "duration": i.duration,
            "genres": i.genres
        }

    albums_list = []

    for album in albums:
        album_data = albums_data[album.id]
        album_data["album"] = album
        albums_list.append(album_data)

    return albums_list
