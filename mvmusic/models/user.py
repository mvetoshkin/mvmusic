from sqlalchemy import Boolean, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class User(BaseModel):
    username = mapped_column(String, nullable=False, unique=True, index=True)
    password = mapped_column(String, nullable=False)
    is_admin = mapped_column(Boolean, nullable=False, default=False)

    libraries = relationship(
        "Library",
        secondary="user_library",
        lazy="joined",
        order_by="Library.name"
    )
