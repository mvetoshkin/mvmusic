import binascii
import hashlib
import importlib
import logging
import time
from pathlib import Path

from flask import Blueprint, g, request
from sqlalchemy import Engine, event, select
from sqlalchemy.exc import NoResultFound
from werkzeug import exceptions as exc

from mvmusic.api import views
from mvmusic.api.libs.exceptions import AppException
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.error import error_serializer
from mvmusic.libs.database import session
from mvmusic.models.client import Client
from mvmusic.models.user import User
from mvmusic.settings import DEBUG, DEBUG_SQL

bp = Blueprint("subsonic_api", __name__, url_prefix="/rest")
logger = logging.getLogger(__name__)


@bp.before_request
def before_request():
    if DEBUG:
        g.start = time.time()

    g.resp_format = request.values.get("f", "xml").lower()
    if g.resp_format not in ("json", "xml"):
        raise exc.BadRequest("Format not supported")


@bp.before_request
def get_current_user():
    if "u" not in request.values:
        return

    username = request.values["u"]

    try:
        query = select(User).where(User.username == username)
        user = session.scalars(query).unique().one()
    except NoResultFound:
        raise exc.Unauthorized

    if "p" in request.values:
        password = request.values["p"]
        if password.startswith("enc:"):
            password = binascii.unhexlify(password[4:]).decode()
        if password != user.password:
            raise exc.Unauthorized

    else:
        salt = request.values["s"]
        token1 = request.values["t"]
        token2 = hashlib.md5(f"{user.password}{salt}".encode()).hexdigest()

        if token1 != token2:
            raise exc.Unauthorized

    g.current_user = user


@bp.before_request
def get_current_client():
    if not g.current_user:
        return

    client = request.values["c"]

    try:
        query = select(Client).where(
            Client.name == client,
            Client.user_id == g.current_user.id
        )
        client_obj = session.scalars(query).one()

    except NoResultFound:
        client_obj = Client(name=client, user_id=g.current_user.id)
        session.add(client_obj)

    g.current_client = client_obj


if DEBUG:
    @bp.after_request
    def after_request(response):
        if DEBUG:
            diff = time.time() - g.start
            logger.debug(f"Request finished in {diff}")

        return response


@bp.teardown_request
def teardown_request(exception):
    if exception:
        session.rollback()
    else:
        session.commit()

    session.remove()


@bp.errorhandler(Exception)
def error_handler(error):
    session.rollback()

    if isinstance(error, exc.HTTPException):
        errors_text = error.name
        status_code = error.code
    else:
        errors_text = "Unknown error"
        status_code = 500

    if status_code == 500:
        logger.error(errors_text, exc_info=True)

    data = {
        "error": error_serializer(status_code, errors_text)
    }

    return make_response(data, status_code)


if DEBUG_SQL:
    # noinspection PyUnusedLocal
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context,
                              executemany):
        conn.info.setdefault("query_start_time", []).append(time.time())
        logger.debug(f"Start Query: {statement}. With parameters: {parameters}")


    # noinspection PyUnusedLocal
    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context,
                             executemany):
        total = time.time() - conn.info["query_start_time"].pop(-1)
        logger.debug(f"Query Complete. Total Time: {str(total)}\n")


for file in Path(views.__file__).parent.iterdir():
    if not file.name.startswith("__") and file.suffix == ".py":
        importlib.import_module(f"{views.__package__}.{file.stem}")
