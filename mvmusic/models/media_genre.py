from sqlalchemy import Column, ForeignKey, String

from mvmusic.models import BaseModel


class MediaGenre(BaseModel):
    id_ = None

    media_id = Column(
        String,
        ForeignKey('media.id', ondelete='cascade'),
        nullable=False,
        primary_key=True
    )

    genre_id = Column(
        String,
        ForeignKey('genre.id', ondelete='cascade'),
        nullable=False,
        primary_key=True
    )
