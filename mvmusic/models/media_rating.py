from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class MediaRating(BaseModel):
    rating = mapped_column(Integer, nullable=False)

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
    "ix_media_rating_media_id_user_id",
    MediaRating.media_id,
    MediaRating.user_id,
    unique=True
)
