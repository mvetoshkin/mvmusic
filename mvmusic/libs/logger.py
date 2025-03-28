import logging.config

from mvmusic.settings import DEBUG, LOGGING, TEST


class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return not DEBUG


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return DEBUG


class RequireTestFalse(logging.Filter):
    def filter(self, record):
        return not TEST


def init_logger():
    logging.config.dictConfig(LOGGING)

