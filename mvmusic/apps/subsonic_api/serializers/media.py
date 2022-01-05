from mvmusic.models.media import Media


def media_serializer(child: Media):
    return {
        'id': child.id_,
        'parent': child.parent_id,
        'isDir': False,
        'title': child.title,
        'album': child.album.name,
        'artist': child.artist.name,
        'track': child.track,
        'year': child.year,
        'genre': child.genres[0].name if child.genres else None,
        'coverArt': child.image_id,
        'size': child.size,
        'contentType': child.content_type,
        'suffix': child.path.split('/')[-1].rpartition('.')[-1],
        'duration': child.duration,
        'bitRate': child.bitrate,
        'path': child.path,
        'isVideo': child.is_video,
        'albumId': child.album_id,
        'artistId': child.artist_id
    }
