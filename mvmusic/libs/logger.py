import logging

from mvmusic.settings import DEBUG


def init_logger():
    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
