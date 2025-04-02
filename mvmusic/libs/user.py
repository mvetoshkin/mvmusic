import logging

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from mvmusic.libs.database import session
from mvmusic.models.library import Library
from mvmusic.models.user import User

logger = logging.getLogger(__name__)


def list_users():
    query = select(User)
    for user in session.scalars(query).unique():
        admin = "admin" if user.is_admin else "not admin"
        print(f"{user.id} | {user.username} | {admin}")


def add_user(name, password, admin=False):
    try:
        query = select(User).where(User.username == name)
        session.scalars(query).one()
        logger.error("User with given name exists")
        return
    except NoResultFound:
        pass

    user = User(username=name, password=password, is_admin=admin)
    session.add(user)

    logger.info(f"User {user.username} added")

    return user


def modify_user(user_id, name=None, password=None, admin=None):
    try:
        user = session.get(User, user_id)
    except NoResultFound:
        logger.error(f"User {user_id} not found")
        return

    if name is not None:
        user.username = name

    if password is not None:
        user.password = password

    if admin is not None:
        user.is_admin = admin


def add_user_library(user_id, library_id):
    try:
        user = session.get(User, user_id)
    except NoResultFound:
        logger.info("User not found")
        return

    try:
        library = session.get(Library, library_id)
    except NoResultFound:
        logger.info("Library not found")
        return

    user.libraries.append(library)

    logger.info(f"Library {library.name} was added to user {user.username}")
