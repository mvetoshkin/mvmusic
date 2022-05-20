from mvmusic.libs import omit_nulls
from mvmusic.models.directory import Directory


def child_serializer(child):
    genres = None
    if hasattr(child, 'genres'):
        genres_list = {i.name for i in child.genres}
        genres = ', '.join(i for i in sorted(genres_list))

    is_dir = isinstance(child, Directory)

    resp = {
        'id': child.id_,
        'parent': child.parent_id,
        'isDir': is_dir,
        'title': child.name if is_dir else child.title,
        'album': child.album.name if hasattr(child, 'album') else None,
        'artist': child.artist.name if hasattr(child, 'artist') else None,
        'track': getattr(child, 'track'),
        'year': getattr(child, 'year'),
        'genre': genres,
        'coverArt': getattr(child, 'image_id'),
        'size': getattr(child, 'size'),
        'contentType': getattr(child, 'content_type'),
        'suffix': getattr(child, 'suffix'),
        'duration': getattr(child, 'duration'),
        'bitRate': getattr(child, 'bitrate'),
        'path': getattr(child, 'path'),
        'isVideo': getattr(child, 'is_video'),
        'discNumber': getattr(child, 'disc_number'),
        'created': getattr(child, 'created_date'),
        'albumId': getattr(child, 'album_id'),
        'artistId': getattr(child, 'artist_id')
    }

    return omit_nulls(resp, {'isDir', 'title'})
