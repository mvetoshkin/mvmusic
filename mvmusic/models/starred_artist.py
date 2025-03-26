from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class StarredArtist(BaseModel):
    artist_id = mapped_column(
        String,
        ForeignKey("artist.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    artist = relationship("Artist", innerjoin=True, uselist=False)
    user = relationship("User", innerjoin=True, uselist=False)


Index(
    "ix_starred_artist_artist_id_user_id",
    StarredArtist.artist_id,
    StarredArtist.user_id,
    unique=True
)
