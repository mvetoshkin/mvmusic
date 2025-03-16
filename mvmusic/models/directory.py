from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, ImageMixin, PathMixin


class Directory(PathMixin, ImageMixin, BaseModel):
    name = mapped_column(String, nullable=False)

    children = relationship(
        "Directory",
        lazy="dynamic",
        viewonly=True,
        order_by="Directory.path.asc()"
    )

    media = relationship(
        "Media",
        lazy="dynamic",
        viewonly=True,
        order_by="Media.track.asc(), Media.title.asc()"
    )
