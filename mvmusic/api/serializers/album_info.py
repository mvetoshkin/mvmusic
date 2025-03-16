from flask import request, url_for

from mvmusic.libs import omit_nulls


def album_info_serializer(album):
    img_host = request.host_url[:-1]
    img_path = url_for("subsonic_api.get_cover_art_view", id=album.image_id)

    resp = {
        "notes": album.notes,
        "musicBrainzId": album.music_brainz_id,
        "lastFmUrl": album.last_fm_url,
        "largeImageUrl": f"{img_host}{img_path}"
    }

    return omit_nulls(resp)
