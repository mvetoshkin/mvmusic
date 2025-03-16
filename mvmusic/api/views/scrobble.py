from flask import g, request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from mvmusic.api.libs.decorators import auth_required, route
from mvmusic.api.libs.responses import make_response
from mvmusic.libs import utcnow
from mvmusic.libs.database import session
from mvmusic.models.history import History
from mvmusic.models.media import Media


@route("/scrobble")
@auth_required
def scrobble_view():
    submission = request.values.get("submission", "1").lower()
    media = session.get_one(Media, request.values["id"])
    now_playing = submission in ("false", "0")
    scrobble_local(media, now_playing)
    return make_response()


def scrobble_local(media, now_playing):
    try:
        query = select(History).where(
            History.client_id == g.current_client.id,
            History.user_id == g.current_user.id,
            History.media_id == media.id,
            History.now_playing == True
        )

        history = session.scalars(query).unique().one()
        history.modified_at = utcnow()
        history.now_playing = now_playing

    except NoResultFound:
        history = History(
            client_id=g.current_client.id,
            user_id=g.current_user.id,
            media_id=media.id,
            now_playing=now_playing
        )
        session.add(history)

    return history
