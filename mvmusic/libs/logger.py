import logging

from mvmusic.settings import DEBUG, DEBUG_SQL


def init_logger():
    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    if DEBUG_SQL:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
