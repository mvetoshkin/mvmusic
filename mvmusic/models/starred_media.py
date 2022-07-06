from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, UserModel


class StarredMedia(BaseModel, UserModel):
    media_id: Column = Column(
        String,
        ForeignKey('media.id', ondelete='cascade'),
        index=True
    )

    media = relationship('Media', uselist=False, lazy='joined')
