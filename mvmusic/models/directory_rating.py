from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class DirectoryRating(BaseModel):
    rating = mapped_column(Integer, nullable=False)

    directory_id = mapped_column(
        String,
        ForeignKey("directory.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    directory = relationship("Directory", innerjoin=True, uselist=False)
    user = relationship("User", innerjoin=True, uselist=False)


Index(
    "ix_directory_rating_directory_id_user_id",
    DirectoryRating.directory_id,
    DirectoryRating.user_id,
    unique=True
)
