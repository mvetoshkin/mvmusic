from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel


class MusicLibrary(BaseModel):
    name = Column(
        String(255),
        nullable=False
    )

    path = Column(
        String,
        nullable=False,
        unique=True
    )

    last_scan = Column(
        DateTime
    )

    users = relationship(
        'User',
        secondary='user_music_library',
        lazy='dynamic',
        viewonly=True
    )
