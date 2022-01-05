import logging
import os

from mvmusic.common.exceptions import NotFoundError
from mvmusic.models.library import Library

logger = logging.getLogger(__name__)


def list_libraries():
    for lib in Library.query.all():
        print(f'{lib.id_:40} {lib.name:20} {lib.path}')


def add_library(path, name):
    if not name:
        name = path.rpartition(os.path.sep)[-1]

    try:
        Library.query.get_by(path=path)
        logger.info('Library with given path exists')
        return
    except NotFoundError:
        pass

    if not os.path.exists(path):
        raise NotFoundError('Given path not found')

    library = Library.create(
        path=path,
        name=name
    )

    logger.info(f'Library {library} added')

    return library
