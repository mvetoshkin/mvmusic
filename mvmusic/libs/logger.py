import logging.config

from mvmusic.settings import DEBUG, LOGGING


class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return not DEBUG


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return DEBUG


def init_logger():
    logging.config.dictConfig(LOGGING)

