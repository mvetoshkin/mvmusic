from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class StarredMedia(BaseModel):
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

    media = relationship("Media", innerjoin=True, uselist=False)
    user = relationship("User", innerjoin=True, uselist=False)


Index(
    "ix_starred_media_media_id_user_id",
    StarredMedia.media_id,
    StarredMedia.user_id,
    unique=True
)
