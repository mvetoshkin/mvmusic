from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import declared_attr, mapped_column, relationship

from mvmusic.models import BaseModel


class DirectoryRating(BaseModel):
    rating = mapped_column(Integer, nullable=False)

    directory_id = mapped_column(
        String,
        ForeignKey("directory.id", ondelete="cascade"),
        nullable=False
    )

    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False
    )

    @declared_attr
    def directory(self):
        return relationship("Directory", innerjoin=True, uselist=False)

    @declared_attr
    def user(self):
        return relationship("User", innerjoin=True, uselist=False)


Index("ix_directory_rating_directory_id", DirectoryRating.directory_id)
Index("ix_directory_rating_user_id", DirectoryRating.user_id)

Index(
    "ix_directory_rating_directory_id_user_id",
    DirectoryRating.directory_id,
    DirectoryRating.user_id,
    unique=True
)
