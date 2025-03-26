import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Common settings

CACHE_PATH = Path(os.environ["MVMUSIC_CACHE_PATH"]).absolute()
DEBUG = os.environ.get("MVMUSIC_DEBUG", "false") == "true"
DISCOGS_ACCESS_TOKEN = os.environ["MVMUSIC_DISCOGS_ACCESS_TOKEN"]
LOGS_DIR = Path(os.environ.get("MVMUSIC_LOGS_DIR", "")).absolute()
MEDIA_PATH = Path(os.environ["MVMUSIC_MEDIA_PATH"]).absolute()
MIGRATIONS_EXCLUDE_TABLES = []
SQLALCHEMY_DATABASE_URI = os.environ["MVMUSIC_SQLALCHEMY_DATABASE_URI"]

# Subsonic API

SECRET_KEY = os.environ["MVMUSIC_SECRET_KEY"]
SUBSONIC_API_IGNORE_ARTICLES = "The El La Los Las Le Les"
TRANSCODE_CMD = "/usr/bin/ffmpeg -i \"{file}\" -ab {bitrate}k -v 0 -f {fmt} -"

# Logging

LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "filters": {
        "require_debug_true": {
            "()": "mvmusic.libs.logger.RequireDebugTrue"
        },
        "require_debug_false": {
            "()": "mvmusic.libs.logger.RequireDebugFalse"
        }
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler"
        },
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "simple",
            "level": "DEBUG"
        },
        "logfile": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filters": ("require_debug_false",),
            "formatter": "simple",
            "level": "INFO",
            "filename": LOGS_DIR / "mvmusic.log",
            "when": "D",
            "backupCount": 7
        }
    },
    "root": {
        "handlers": ["console", "logfile"],
        "level": "DEBUG"
    },
    "loggers": {
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": "INFO"
        }
    }
}
