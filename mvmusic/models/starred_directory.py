from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, UserModel


class StarredDirectory(BaseModel, UserModel):
    directory_id: Column = Column(
        String,
        ForeignKey('directory.id', ondelete='cascade'),
        index=True
    )

    directory = relationship('Directory', uselist=False, lazy='joined')
