from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, UserMixin


class StarredArtist(UserMixin, BaseModel):
    artist_id = mapped_column(
        String,
        ForeignKey("artist.id", ondelete="cascade"),
        index=True
    )

    artist = relationship(
        "Artist",
        uselist=False,
        lazy="joined"
    )
