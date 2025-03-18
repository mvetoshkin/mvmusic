from flask import g, request
from sqlalchemy import func, nullslast, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import noload
from werkzeug.exceptions import BadRequest, Forbidden

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.album_list import album_list_serializer
from mvmusic.libs.database import session
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.directory import Directory
from mvmusic.models.directory_rating import DirectoryRating
from mvmusic.models.genre import Genre
from mvmusic.models.history import History
from mvmusic.models.media import Media
from mvmusic.models.media_genre import MediaGenre
from mvmusic.models.starred_directory import StarredDirectory


@route("/getAlbumList")
@auth_required
def get_album_list_view():
    list_type = request.values["type"]

    size = int(request.values.get("size", "10"))
    size = max(size, 1)
    size = min(size, 500)

    offset = int(request.values.get("offset", "0"))

    music_folder_id = request.values.get("musicFolderId")
    library_ids = [i.id for i in g.current_user.libraries]
    if music_folder_id:
        if music_folder_id not in library_ids:
            raise Forbidden
        library_ids = [music_folder_id]

    if list_type == "random":
        query = select(Directory).where(Directory.library_id.in_(library_ids))
        query = query.order_by(func.random())
        query = query.limit(size)
        query = query.offset(size * offset)

        dirs = [i for i in session.scalars(query).unique()]
        data = album_list_serializer(dirs)
        return make_response({"albumList": data})

    if list_type == "newest":
        query = select(Directory, Media.year).distinct()
        query = query.join(Media)
        query = query.where(Media.year != None)
        query = query.order_by(Media.year.desc(), Directory.name)

    elif list_type == "highest":
        avg_sq = select(
            DirectoryRating.directory_id,
            func.sum(1).label("avg_rating")
        )
        avg_sq = avg_sq.where(DirectoryRating.user_id == g.current_user.id)
        avg_sq = avg_sq.group_by(DirectoryRating.directory_id)
        avg_sq = avg_sq.subquery()

        query = select(Directory, avg_sq.c.avg_rating).distinct()
        query = query.select_from(Directory)
        query = query.outerjoin(avg_sq)
        query = query.order_by(
            nullslast(avg_sq.c.avg_rating.desc()),
            Directory.name
        )

    elif list_type == "frequent":
        stats_sq = select(History.media_id, func.sum(1).label("plays_count"))
        stats_sq = stats_sq.where(History.user_id == g.current_user.id)
        stats_sq = stats_sq.group_by(History.media_id)
        stats_sq = stats_sq.subquery()

        query = select(Directory, stats_sq.c.plays_count).distinct()
        query = query.select_from(Directory)
        query = query.join(Media)
        query = query.outerjoin(stats_sq)
        query = query.order_by(
            nullslast(stats_sq.c.plays_count.desc()),
            Directory.name
        )

    elif list_type == "recent":
        stats_sq = select(History.media_id,
                          func.max(History.modified_at).label("played_at"))
        stats_sq = stats_sq.where(History.user_id == g.current_user.id)
        stats_sq = stats_sq.group_by(History.media_id)
        stats_sq = stats_sq.subquery()

        query = select(Directory, stats_sq.c.played_at).distinct()
        query = query.select_from(Directory)
        query = query.join(Media)
        query = query.outerjoin(stats_sq)
        query = query.order_by(
            nullslast(stats_sq.c.played_at.desc()),
            Directory.name
        )

    elif list_type == "alphabeticalByName":
        query = select(Directory, Album.name).distinct()
        query = query.select_from(Directory)
        query = query.join(Media)
        query = query.join(Album)
        query = query.order_by(Album.name)

    elif list_type == "alphabeticalByArtist":
        query = select(Directory, Artist.name, Album.name).distinct()
        query = query.select_from(Directory)
        query = query.join(Media)
        query = query.join(Artist, Artist.id == Media.artist_id)
        query = query.join(Album, Album.id == Media.album_id)
        query = query.order_by(Artist.name, Album.name)

    elif list_type == "starred":
        query = select(Directory).distinct()
        query = query.join(StarredDirectory)
        query = query.where(StarredDirectory.user_id == g.current_user.id)
        query = query.order_by(Directory.name)

    elif list_type == "byYear":
        from_year = request.values["fromYear"]
        to_year = request.values["toYear"]

        query = select(Directory, Media.year).distinct()
        query = query.join(Media)
        query = query.where(Media.year != None)

        reverse = False

        if from_year > to_year:
            reverse = True
            from_year, to_year = to_year, from_year

        query = query.where(
            Media.year >= int(from_year),
            Media.year <= int(to_year)
        )

        query = query.order_by(
            Media.year.desc() if reverse else Media.year,
            Directory.name
        )

    elif list_type == "byGenre":
        genre = request.values["genre"]

        try:
            genre_query = select(Genre).where(
                func.lower(Genre.name) == func.lower(genre)  # type: ignore
            )
            genre_obj = session.scalars(genre_query).one()
        except NoResultFound:
            raise BadRequest("Genre not found")

        query = select(Directory).distinct()
        query = query.join(Media)
        query = query.join(MediaGenre)
        query = query.where(MediaGenre.genre_id == genre_obj.id)
        query = query.order_by(Directory.name)

    else:
        raise BadRequest("Unsupported list type")

    query = query.options(noload(Directory.library))
    query = query.where(Directory.library_id.in_(library_ids))
    query = query.limit(size)
    query = query.offset(size * offset)

    albums = [i[0] for i in session.execute(query)]

    data = album_list_serializer(albums)
    return make_response({"albumList": data})
