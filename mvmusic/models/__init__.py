import re
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column

from mvmusic.libs import utcnow


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    created_at = mapped_column(
        DateTime,
        nullable=False,
        default=utcnow
    )

    modified_at = mapped_column(
        DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow
    )

    @declared_attr.directive
    def __tablename__(self):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
