import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from mvmusic.libs.database import session
from mvmusic.models.library import Library

logger = logging.getLogger(__name__)


def list_libraries():
    query = select(Library)
    for lib in session.scalars(query):
        print(f"{lib.id} | {lib.name} | {lib.path}")


def add_library(path, name):
    path = Path(path)
    name = name or path.name

    try:
        query = select(Library).where(Library.path == str(path))
        session.scalars(query).one()
        logger.error("Library with given path exists")
        return
    except NoResultFound:
        pass

    if not path.exists():
        logger.error("Given path not found")
        return

    library = Library(name=name, path=str(path))
    session.add(library)

    logger.info(f"Library {library.name} added")

    return library
