from urllib.parse import unquote_plus, urlparse

from mvmusic.libs import dict_value, get_request


def parse_wikidata(url):
    id_ = url.rpartition("/")[-1]

    resp = get_request("https://www.wikidata.org/w/api.php", params={
        "action": "wbgetentities",
        "props": "sitelinks/urls",
        "ids": id_,
        "format": "json"
    })

    data = resp.json()

    wiki_url = dict_value(data, f"entities.{id_}.sitelinks.ruwiki.url")
    if not wiki_url:
        wiki_url = dict_value(data, f"entities.{id_}.sitelinks.enwiki.url")

    if not wiki_url:
        return {}

    return parse_wiki(wiki_url)


def parse_wiki(url):
    title = unquote_plus(url.rpartition("/")[-1])
    domain = urlparse(url).netloc

    resp = get_request(f"https://{domain}/w/api.php", params={
        "action": "query",
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "titles": title,
        "format": "json"
    })

    data = resp.json()
    pages = list(dict_value(data, "query.pages", {}).values())

    if pages:
        return {
            "notes": pages[0]["extract"]
        }

    return {}
