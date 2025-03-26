from sqlalchemy import Boolean, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class User(BaseModel):
    username = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)
    is_admin = mapped_column(Boolean, default=False, nullable=False)

    clients = relationship("Client", viewonly=True)
    libraries = relationship("Library", secondary="user_library")
