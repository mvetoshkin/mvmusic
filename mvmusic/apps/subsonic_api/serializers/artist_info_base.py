from flask import request, url_for

from mvmusic.libs import omit_nulls


def artist_info_base_serializer(artist):
    resp = {
        'biography': artist.notes,
        'musicBrainzId': artist.music_brainz_id,
        'lastFmUrl': artist.last_fm_url,
        'largeImageUrl': request.host_url[:-1] + url_for(
            'subsonic_api.get_cover_art_view', id_=artist.image_id
        )
    }

    return omit_nulls(resp)
