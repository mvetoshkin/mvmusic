from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel


class History(BaseModel):
    media_id: Column = Column(
        String,
        ForeignKey('media.id', ondelete='cascade'),
        index=True
    )

    user_id: Column = Column(
        String,
        ForeignKey('user.id', ondelete='cascade'),
        index=True
    )

    media = relationship('Media', uselist=False, lazy='joined')
    user = relationship('User', uselist=False, lazy='joined')
