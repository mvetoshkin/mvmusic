from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column

from mvmusic.models import BaseModel


class UserLibrary(BaseModel):
    id = None

    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
        primary_key=True
    )

    library_id = mapped_column(
        String,
        ForeignKey("library.id", ondelete="cascade"),
        nullable=False,
        primary_key=True
    )
