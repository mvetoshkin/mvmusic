import re
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, \
    relationship

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


class PathMixin:
    last_seen = mapped_column(DateTime)
    path = mapped_column(String, nullable=False, index=True)

    library_id = mapped_column(
        String,
        ForeignKey("library.id", ondelete="cascade"),
        nullable=False
    )

    parent_id = mapped_column(
        String,
        ForeignKey("directory.id", ondelete="cascade")
    )

    @declared_attr
    def library(self):
        return relationship("Library", lazy="joined", uselist=False)

    @declared_attr
    def parent(self):
        return relationship(
            "Directory",
            lazy="joined",
            uselist=False,
            remote_side="Directory.id"
        )


class ImageMixin:
    image_id = mapped_column(
        String,
        ForeignKey("image.id", ondelete="set null")
    )

    @declared_attr
    def image(self):
        return relationship("Image", uselist=False)


class UserMixin:
    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
        index=True
    )

    @declared_attr
    def user(self):
        return relationship("User", uselist=False)


class ScannedMixin:
    scanned = mapped_column(Boolean, default=False)
