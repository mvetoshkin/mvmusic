from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel


class Genre(BaseModel):
    name: Column = Column(String, nullable=False, index=True)

    media = relationship(
        'Media',
        secondary='media_genre',
        lazy='dynamic',
        viewonly=True
    )
