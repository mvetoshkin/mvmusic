from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Genre(BaseModel):
    name = mapped_column(String, index=True, nullable=False)

    media = relationship("Media", secondary="media_genre", viewonly=True)
