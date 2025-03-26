from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class History(BaseModel):
    now_playing = mapped_column(Boolean, default=False, nullable=False)

    client_id = mapped_column(
        String,
        ForeignKey("client.id", ondelete="set null"),
        index=True,
        nullable=False
    )

    media_id = mapped_column(
        String,
        ForeignKey("media.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    client = relationship("Client", innerjoin=True, uselist=False)
    media = relationship("Media", innerjoin=True, uselist=False)
    user = relationship("User", innerjoin=True, uselist=False)
