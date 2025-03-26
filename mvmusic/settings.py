import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Common settings

CACHE_PATH = Path(os.environ["MVMUSIC_CACHE_PATH"]).absolute()
DEBUG = os.environ.get("MVMUSIC_DEBUG", "false") == "true"
DEBUG_SQL = os.environ.get("MVMUSIC_DEBUG_SQL", "false") == "true"
DISCOGS_ACCESS_TOKEN = os.environ["MVMUSIC_DISCOGS_ACCESS_TOKEN"]
MEDIA_PATH = Path(os.environ["MVMUSIC_MEDIA_PATH"]).absolute()
MIGRATIONS_EXCLUDE_TABLES = []
SQLALCHEMY_DATABASE_URI = os.environ["MVMUSIC_SQLALCHEMY_DATABASE_URI"]

# Subsonic API

SECRET_KEY = os.environ["MVMUSIC_SECRET_KEY"]
SUBSONIC_API_IGNORE_ARTICLES = "The El La Los Las Le Les"
TRANSCODE_CMD = "/usr/bin/ffmpeg -i \"{file}\" -ab {bitrate}k -v 0 -f {fmt} -"
