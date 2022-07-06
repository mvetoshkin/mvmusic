from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, UserModel


class StarredAlbum(BaseModel, UserModel):
    album_id: Column = Column(
        String,
        ForeignKey('album.id', ondelete='cascade'),
        index=True
    )

    album = relationship('Album', uselist=False, lazy='joined')
