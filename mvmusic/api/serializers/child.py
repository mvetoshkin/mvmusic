import re

from mvmusic.libs import omit_nulls
from mvmusic.models.directory import Directory


def child_serializer(child):
    genres = None
    if hasattr(child, "genres"):
        genres_list = {i.name for i in child.genres}
        genres = ", ".join(i for i in sorted(genres_list))

    is_dir = isinstance(child, Directory)

    artist = child.artist.name if hasattr(child, "artist") else None
    title = child.name if is_dir else child.title
    year = getattr(child, "year", None)

    if is_dir:
        matches = re.match(r"(\d{4})\s(.*)", title)
        if matches:
            year, title = matches.groups()
            artist = child.parent.name

    resp = {
        "id": child.id,
        "parent": child.parent_id,
        "isDir": is_dir,
        "title": title,
        "album": child.album.name if hasattr(child, "album") else None,
        "artist": artist,
        "track": getattr(child, "track", None),
        "year": year,
        "genre": genres,
        "coverArt": getattr(child, "image_id", None),
        "size": getattr(child, "size", None),
        "contentType": getattr(child, "content_type", None),
        "suffix": getattr(child, "suffix", None),
        "duration": getattr(child, "duration", None),
        "bitRate": getattr(child, "bitrate", None),
        "path": getattr(child, "path", None),
        "isVideo": getattr(child, "is_video", None),
        "discNumber": getattr(child, "disc_number", None),
        "created": getattr(child, "created_at", None),
        "albumId": getattr(child, "album_id", None),
        "artistId": getattr(child, "artist_id", None)
    }

    return omit_nulls(resp, {"isDir", "title"})
