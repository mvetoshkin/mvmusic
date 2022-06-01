from urllib.parse import unquote_plus

import requests

from mvmusic.settings import settings


def get_discogs_artist(id_):
    info = make_request(f'/artists/{id_}')

    data = {
        'notes': info['profile'],
        'image_url': get_image(info)
    }

    data.update(get_urls(info))
    return data


def search_discogs_artist(artist):
    response = make_request(f'/database/search', {
        'query': artist.name,
        'type': 'artist'
    })

    if not response.get('results'):
        return None

    artist_id = response['results'][0]['id']
    return get_discogs_artist(artist_id)


def get_discogs_album(id_):
    info = make_request(f'/masters/{id_}')

    data = {
        'image_url': get_image(info)
    }

    data.update(get_urls(info))

    return data


def search_discogs_album(album):
    response = make_request(f'/database/search', {
        'query': album.name,
        'type': 'master',
        'artist': album.artist.name
    })

    if not response.get('results'):
        return None

    album_id = response['results'][0]['id']
    return get_discogs_album(album_id)


def make_request(path, params=None):
    params = params or {}
    api_root = 'https://api.discogs.com' + path
    params['token'] = settings.DISCOGS_ACCESS_TOKEN
    resp = requests.get(api_root, params=params)
    return resp.json()


def get_image(info):
    for image in info.get('images', []):
        if image['type'] == 'primary':
            return unquote_plus(image['uri'])
    return None


def get_urls(info):
    urls = {}

    for url in info.get('urls', []):
        if 'wikipedia' in url.lower():
            urls['wiki_url'] = unquote_plus(url)
        elif 'wikidata' in url.lower():
            urls['wikidata_url'] = unquote_plus(url)

    return urls
