import requests

from mvmusic.models.album import Album
from mvmusic.models.artist import Artist


def get_mb_artist(artist: Artist):
    resp = make_request(f'/artist/{artist.music_brainz_id}', {
        'inc': 'url-rels'
    })

    return get_data(resp)


def get_mb_album(album: Album):
    release = make_request(f'/release/{album.music_brainz_id}', {
        'inc': 'release-groups'
    })

    release_group_id = release['release-group']['id']
    release_group = make_request(f'/release-group/{release_group_id}', {
        'inc': 'url-rels'
    })

    return get_data(release_group)


def make_request(path, params=None):
    params = params or {}
    rul = 'https://musicbrainz.org/ws/2' + path
    params['fmt'] = 'json'
    resp = requests.get(rul, params=params)
    return resp.json()


def get_data(artist):
    data = {}

    for item in artist['relations']:
        if item['type'] == 'discogs':
            data['discogs_id'] = item['url']['resource'].rpartition('/')[-1]
        elif item['type'] == 'last.fm':
            data['last_fm_url'] = item['url']['resource']

    return data
