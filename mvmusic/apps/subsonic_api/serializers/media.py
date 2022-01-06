from mvmusic.models.media import Media


def media_serializer(media: Media):
    return {
        'id': media.id_,
        'parent': media.parent_id,
        'isDir': False,
        'title': media.title,
        'album': media.album.name,
        'artist': media.artist.name,
        'track': media.track,
        'year': media.year,
        'genre': media.genres[0].name if media.genres else None,
        'coverArt': media.image_id,
        'size': media.size,
        'contentType': media.content_type,
        'suffix': media.path.split('/')[-1].rpartition('.')[-1],
        'duration': media.duration,
        'bitRate': media.bitrate,
        'path': media.path,
        'isVideo': media.is_video,
        'albumId': media.album_id,
        'artistId': media.artist_id
    }
