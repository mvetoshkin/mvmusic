from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Genre(BaseModel):
    name = mapped_column(
        String,
        nullable=False,
        index=True
    )

    media = relationship(
        "Media",
        secondary="media_genre",
        lazy="dynamic",
        viewonly=True
    )
