from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, UserMixin


class History(UserMixin, BaseModel):
    now_playing = mapped_column(Boolean, default=False, index=True)

    client_id = mapped_column(
        String,
        ForeignKey("client.id", ondelete="set null"),
        index=True
    )

    media_id = mapped_column(
        String,
        ForeignKey("media.id", ondelete="cascade"),
        index=True
    )

    client = relationship(
        "Client",
        uselist=False,
        lazy="joined"
    )

    media = relationship(
        "Media",
        uselist=False,
        lazy="joined"
    )
