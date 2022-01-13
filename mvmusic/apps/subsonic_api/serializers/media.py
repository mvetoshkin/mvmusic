from mvmusic.libs import omit_nulls
from mvmusic.models.media import Media


def media_serializer(media: Media, type_='music'):
    genres = None
    if media.genres:
        genres_list = {i.name for i in media.genres}
        genres = ', '.join(i for i in sorted(genres_list))

    resp = {
        'id': media.id_,
        'parent': media.parent_id,
        'isDir': False,
        'title': media.title,
        'album': media.album.name if media.album else None,
        'artist': media.artist.name if media.artist else None,
        'track': media.track,
        'year': media.year,
        'genre': genres,
        'coverArt': media.image_id,
        'size': media.size,
        'contentType': media.content_type,
        'suffix': media.suffix,
        'duration': media.duration,
        'bitRate': media.bitrate,
        'path': media.path,
        'isVideo': media.is_video,
        'albumId': media.album_id,
        'artistId': media.artist_id,
        'created': media.created_date,
        'discNumber': media.disc_number,
        'type': type_
    }

    return omit_nulls(resp, {'isDir', 'title'})
