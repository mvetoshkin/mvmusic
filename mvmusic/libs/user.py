import logging

from mvmusic.common.exceptions import NotFoundError
from mvmusic.models.library import Library
from mvmusic.models.user import User

logger = logging.getLogger(__name__)


def list_users():
    for user in User.query.all():
        admin = 'admin' if user.is_admin else ''
        print(f'{user.id_:40} {user.username:20} {admin}')


def add_user(name, password, admin):
    try:
        User.query.get_by(username=name)
        logger.info('User with given name exists')
        return
    except NotFoundError:
        pass

    user = User.create(
        username=name,
        password=password,
        is_admin=admin
    )

    logger.info(f'User {user} added')

    return user


def modify_user(id_, name, password, admin):
    try:
        user = User.query.get(id_)
    except NotFoundError:
        logger.info('User not found')
        return

    if name is not None:
        user.username = name

    if password is not None:
        user.password = password

    if admin is not None:
        user.is_admin = admin


def add_library(user_id, library_id):
    try:
        user = User.query.get(user_id)
    except NotFoundError:
        logger.info('User not found')
        return

    try:
        library = Library.query.get(library_id)
    except NotFoundError:
        logger.info('Library not found')
        return

    user.libraries.append(library)

    logger.info(f'Library {library} was added to user {user}')
