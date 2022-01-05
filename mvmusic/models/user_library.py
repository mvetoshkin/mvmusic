from sqlalchemy import Column, ForeignKey, String

from mvmusic.models import BaseModel


class UserLibrary(BaseModel):
    id_ = None

    user_id = Column(
        String,
        ForeignKey('user.id', ondelete='cascade'),
        nullable=False,
        primary_key=True
    )

    library_id = Column(
        String,
        ForeignKey('library.id', ondelete='cascade'),
        nullable=False,
        primary_key=True
    )
