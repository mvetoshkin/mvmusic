from sqlalchemy import Column, String, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, ImageModel, PathModel


class Media(BaseModel, PathModel, ImageModel):
    title: Column = Column(String)
    year = Column(Numeric)
    track = Column(Numeric)
    duration = Column(Numeric)
    bitrate = Column(Numeric)
    size = Column(Numeric)
    content_type = Column(String)
    is_video = Column(Boolean)

    album_id: Column = Column(
        String,
        ForeignKey('album.id', ondelete='cascade')
    )

    artist_id = Column(
        String,
        ForeignKey('artist.id', ondelete='cascade')
    )

    album = relationship('Album', uselist=False, lazy='joined')
    artist = relationship('Artist', uselist=False, lazy='joined')
    genres = relationship('Genre', secondary='media_genre', lazy='joined')
