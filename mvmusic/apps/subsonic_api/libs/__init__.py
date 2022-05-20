import re
from xml.etree import ElementTree

from mvmusic.settings import settings


def ignored_articles():
    ignored = settings.SUBSONIC_API_IGNORE_ARTICLES
    if not ignored:
        return None

    chunks = ignored.split(' ')
    reg_exp = '^(' + ' |'.join(re.escape(i) for i in chunks) + ')'

    return re.compile(reg_exp, re.IGNORECASE)


def dict2xml(element, dictionary):
    for key, value in dictionary.items():
        if key == 'value':
            element.text = value_tostring(value)

        elif isinstance(value, dict):
            sub_element = ElementTree.SubElement(element, key)
            dict2xml(sub_element, value)

        elif isinstance(value, list):
            for v in value:
                sub_element = ElementTree.SubElement(element, key)

                if isinstance(v, dict):
                    dict2xml(sub_element, v)
                else:
                    sub_element.text = value_tostring(v)

        else:
            element.set(key, value_tostring(value))


def value_tostring(value):
    if value is None:
        return None

    if isinstance(value, str):
        return value

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)
