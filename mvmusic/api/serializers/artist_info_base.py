from flask import request, url_for

from mvmusic.libs import omit_nulls


def artist_info_base_serializer(artist):
    img_host = request.host_url[:-1]
    img_path = url_for("subsonic_api.get_cover_art_view", id=artist.image_id)

    resp = {
        "biography": artist.notes,
        "musicBrainzId": artist.music_brainz_id,
        "lastFmUrl": artist.last_fm_url,
        "largeImageUrl": f"{img_host}{img_path}"
    }

    return omit_nulls(resp)
