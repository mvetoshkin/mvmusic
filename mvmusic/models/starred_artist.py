from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, UserModel


class StarredArtist(BaseModel, UserModel):
    artist_id: Column = Column(
        String,
        ForeignKey('artist.id', ondelete='cascade'),
        index=True
    )

    artist = relationship('Artist', uselist=False, lazy='joined')
