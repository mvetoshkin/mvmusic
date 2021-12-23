from sqlalchemy import Column, ForeignKey, String

from mvmusic.models import BaseModel


class UserMusicLibrary(BaseModel):
    id_ = None

    user_id = Column(
        String,
        ForeignKey('user.id', ondelete='cascade'),
        nullable=False,
        primary_key=True
    )

    music_library_id = Column(
        String,
        ForeignKey('music_library.id', ondelete='cascade'),
        nullable=True,
        primary_key=True
    )
