import logging

from mvmusic.settings import settings


def init_logger():
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    )
