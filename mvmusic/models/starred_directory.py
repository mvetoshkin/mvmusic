from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class StarredDirectory(BaseModel):
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
    "ix_starred_directory_directory_id_user_id",
    StarredDirectory.directory_id,
    StarredDirectory.user_id,
    unique=True
)
