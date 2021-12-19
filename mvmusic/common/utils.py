import importlib
import os

from dotenv import load_dotenv

import mvmusic
from mvmusic import settings as settings_
from mvmusic.common.exceptions import NoSettingsModuleSpecified


# noinspection PyPep8Naming
class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def import_object(path):
    module_name, object_name = path.rsplit('.', 1)
    mod = importlib.import_module(module_name)
    if not hasattr(mod, object_name):
        raise ImportError

    return getattr(mod, object_name)


def to_camel_case(text):
    text = text.replace('-', ' ').replace('_', ' ').lower()
    if not text:
        return text

    chunks = text.split()
    return chunks[0] + ''.join(i.capitalize() for i in chunks[1:])


def get_settings():
    path = os.path.dirname(mvmusic.__file__)
    env_path = os.path.join(path, '.env')

    if os.path.exists(env_path):
        load_dotenv(env_path)

    app_settings = os.environ.get('MVMUSIC_SETTINGS', False)
    if not app_settings:
        raise NoSettingsModuleSpecified(
            'Path to settings module is not found'
        )

    obj = getattr(settings_, app_settings)
    return obj()


settings = get_settings()
