from sqlalchemy import Column, DateTime, String

from mvmusic.common.models import BaseModel


class User(BaseModel):
    username = Column(
        String(128),
        nullable=False,
        unique=True,
        index=True
    )

    password = Column(
        String(128),
        nullable=False
    )

    deleted = Column(
        DateTime,
        index=True,
        nullable=False,
        default=False
    )

    email = Column(
        String(128),
        unique=True
    )
