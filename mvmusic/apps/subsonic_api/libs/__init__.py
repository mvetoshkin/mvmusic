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


def get_subsonic_error_code(status):
    statuses = {
        400: 10,
        401: 40,
        403: 50,
        404: 70,
    }

    return statuses.get(status, 0)


def dict2xml(element, dictionary):
    for name, value in dictionary.items():
        if name == 'value':
            element.text = value_tostring(value)

        elif isinstance(value, dict):
            sub_element = ElementTree.SubElement(element, name)
            dict2xml(sub_element, value)

        elif isinstance(value, list):
            for v in value:
                sub_element = ElementTree.SubElement(element, name)

                if isinstance(v, dict):
                    dict2xml(sub_element, v)
                else:
                    sub_element.text = value_tostring(v)

        else:
            element.set(name, value_tostring(value))


def value_tostring(value):
    if value is None:
        return None

    if isinstance(value, str):
        return value

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)
