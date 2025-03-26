from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class StarredAlbum(BaseModel):
    album_id = mapped_column(
        String,
        ForeignKey("album.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    album = relationship("Album", innerjoin=True, uselist=False)
    user = relationship("User", innerjoin=True, uselist=False)


Index(
    "ix_starred_album_album_id_user_id",
    StarredAlbum.album_id,
    StarredAlbum.user_id,
    unique=True
)
