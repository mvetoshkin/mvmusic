import os

from dotenv import load_dotenv

import mvmusic
from mvmusic.libs.exceptions import NoSettingsModuleSpecified


class DefaultSettings:
    BLUEPRINTS = (
        'mvmusic.apps.general.urls.bp',
        'mvmusic.apps.subsonic_api.urls.bp',
    )

    CACHE_PATH = '/var/cache/mvmusic'
    DEBUG = False
    DEBUG_SQL = False
    ENV = 'production'

    EXTENSIONS = (
        'mvmusic.libs.extensions.cors',
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUBSONIC_API_IGNORE_ARTICLES = 'The El La Los Las Le Les'
    TRANSCODE_CMD = '/usr/bin/ffmpeg -i "{file}" -ab {bitrate}k -v 0 -f {fmt} -'

    # noinspection PyPep8Naming
    @property
    def DISCOGS_ACCESS_TOKEN(self):
        return os.environ.get('DISCOGS_ACCESS_TOKEN')

    # noinspection PyPep8Naming
    @property
    def SECRET_KEY(self):
        return os.environ['MVMUSIC_SECRET_KEY']

    # noinspection PyPep8Naming
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'postgresql://{}:{}@{}/{}'.format(
            os.environ['DB_USER'], os.environ['DB_PASSWORD'],
            os.environ['DB_HOST'], os.environ['DB_NAME'])


class DevelopmentSettings(DefaultSettings):
    DEBUG = True
    DEBUG_SQL = DEBUG
    CACHE_PATH = os.path.join(
        os.path.dirname(mvmusic.__file__).rpartition(os.path.sep)[0], '.cache'
    )
    ENV = 'development'
    TRANSCODE_CMD = '/usr/local/bin/ffmpeg -i "{file}" -ab {bitrate}k -v 0 ' \
                    '-f {fmt} -'


class ProductionSettings(DefaultSettings):
    pass


###

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

    return globals()[app_settings]()


settings = get_settings()
