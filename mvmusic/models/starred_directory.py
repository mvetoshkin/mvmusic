from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, UserMixin


class StarredDirectory(UserMixin, BaseModel):
    directory_id = mapped_column(
        String,
        ForeignKey("directory.id", ondelete="cascade"),
        index=True
    )

    directory = relationship(
        "Directory",
        uselist=False,
        lazy="joined"
    )
