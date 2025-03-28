from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.api.serializers.user import user_serializer
from mvmusic.libs.database import session
from mvmusic.models.user import User


@route("/getUser")
@auth_required
def get_user_view():
    """Get details about a given user, including which authorization roles
    and folder access it has. Can be used to enable/disable certain features
    in the client."""

    username = request.values["username"]

    if not g.current_user.is_admin and g.current_user.username != username:
        raise NotFound

    try:
        query = select(User).where(User.username == username)
        user = session.scalars(query).one()
    except NoResultFound:
        raise NotFound

    data = user_serializer(user)
    return make_response({"user": data})
