from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column

from mvmusic.models import BaseModel


class MediaGenre(BaseModel):
    id = None

    genre_id = mapped_column(
        String,
        ForeignKey("genre.id", ondelete="cascade"),
        nullable=False,
        primary_key=True
    )

    media_id = mapped_column(
        String,
        ForeignKey("media.id", ondelete="cascade"),
        nullable=False,
        primary_key=True
    )
