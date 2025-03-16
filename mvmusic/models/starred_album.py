from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, UserMixin


class StarredAlbum(UserMixin, BaseModel):
    album_id = mapped_column(
        String,
        ForeignKey("album.id", ondelete="cascade"),
        index=True
    )

    album = relationship(
        "Album",
        uselist=False,
        lazy="joined"
    )
