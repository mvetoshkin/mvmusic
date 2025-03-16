from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, UserMixin


class StarredMedia(UserMixin, BaseModel):
    media_id = mapped_column(
        String,
        ForeignKey("media.id", ondelete="cascade"),
        index=True
    )

    media = relationship(
        "Media",
        uselist=False,
        lazy="joined"
    )
