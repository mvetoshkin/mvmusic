from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Library(BaseModel):
    name = mapped_column(String, nullable=False)
    path = mapped_column(String, nullable=False, unique=True)

    directories = relationship(
        "Directory",
        lazy="dynamic",
        viewonly=True
    )

    media = relationship(
        "Media",
        lazy="dynamic",
        viewonly=True
    )

    users = relationship(
        "User",
        secondary="user_library",
        lazy="dynamic",
        viewonly=True
    )
