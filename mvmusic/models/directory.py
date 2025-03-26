from sqlalchemy import DateTime, ForeignKey, String, Index
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Directory(BaseModel):
    last_seen = mapped_column(DateTime, index=True, nullable=False)
    name = mapped_column(String, nullable=False)
    path = mapped_column(String, nullable=False, unique=True)

    image_id = mapped_column(
        String,
        ForeignKey("image.id", ondelete="set null"),
        index=True
    )

    library_id = mapped_column(
        String,
        ForeignKey("library.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    parent_id = mapped_column(
        String,
        ForeignKey("directory.id", ondelete="cascade"),
        index=True
    )

    children = relationship(
        "Directory",
        order_by="Directory.name",
        viewonly=True
    )

    image = relationship("Image", uselist=False)
    library = relationship("Library", innerjoin=True, uselist=False)
    media = relationship("Media", order_by="Media.title", viewonly=True)

    parent = relationship(
        "Directory",
        uselist=False,
        remote_side="Directory.id"
    )


Index(
    "ix_directory_library_id_path",
    Directory.library_id,
    Directory.path,
    unique=True
)
