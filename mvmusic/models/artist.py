from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, ImageModel


class Artist(BaseModel, ImageModel):
    name = Column(String, nullable=False, index=True)
    notes: Column = Column(String)
    music_brainz_id = Column(String)
    last_fm_url = Column(String)

    albums = relationship(
        'Album',
        lazy='dynamic',
        viewonly=True,
        order_by='Album.year.asc(), Album.name.asc()'
    )

    media = relationship('Media', lazy='dynamic', viewonly=True)
