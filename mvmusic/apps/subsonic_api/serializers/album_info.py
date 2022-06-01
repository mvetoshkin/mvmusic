from flask import request, url_for

from mvmusic.libs import omit_nulls


def album_info_serializer(album):
    resp = {
        'notes': album.notes,
        'musicBrainzId': album.music_brainz_id,
        'lastFmUrl': album.last_fm_url,
        'largeImageUrl': request.host_url[:-1] + url_for(
            'subsonic_api.get_cover_art_view', id_=album.image_id
        )
    }

    return omit_nulls(resp)
