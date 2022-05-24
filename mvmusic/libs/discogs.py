import requests

from mvmusic.settings import settings


def get_discogs_artist(id_):
    info = make_request(f'/artists/{id_}')

    return {
        'notes': info['profile'],
        'image_url': get_image(info)
    }


def search_discogs_artist(name):
    response = make_request(f'/database/search', {
        'query': name,
        'type': 'artist'
    })

    if not response.get('results'):
        return None

    artist_id = response['results'][0]['id']
    return get_discogs_artist(artist_id)


def get_discogs_album(id_):
    info = make_request(f'/masters/{id_}')

    return {
        'notes': info['notes'],
        'image_url': get_image(info)
    }


def search_discogs_album(artist_name, album_name):
    response = make_request(f'/database/search', {
        'query': album_name,
        'type': 'master',
        'artist': artist_name
    })

    album_id = response['results'][0]['id']
    return get_discogs_album(album_id)


def make_request(path, params=None):
    params = params or {}
    api_root = 'https://api.discogs.com' + path
    params['token'] = settings.DISCOGS_ACCESS_TOKEN
    resp = requests.get(api_root, params=params)
    return resp.json()


def get_image(info):
    for image in info['images']:
        if image['type'] == 'primary':
            return image['uri']
    return None
