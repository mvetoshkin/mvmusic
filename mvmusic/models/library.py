from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel


class Library(BaseModel):
    name = Column(String(255), nullable=False)
    path = Column(String, nullable=False, unique=True)

    directories = relationship('Directory', lazy='dynamic', viewonly=True)
    media = relationship('Media', lazy='dynamic', viewonly=True)
    users = relationship('User', secondary='user_library', lazy='dynamic',
                         viewonly=True)
