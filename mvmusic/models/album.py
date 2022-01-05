from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, ImageModel


class Album(BaseModel, ImageModel):
    name = Column(String, nullable=False, index=True)
    notes: Column = Column(String)
    music_brainz_id = Column(String)

    artist_id = Column(
        String,
        ForeignKey('artist.id', ondelete='cascade'),
        nullable=False
    )

    artist = relationship('Artist', uselist=False, lazy='joined')