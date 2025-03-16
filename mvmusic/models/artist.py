from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, ImageMixin, ScannedMixin


class Artist(ImageMixin, ScannedMixin, BaseModel):
    name = mapped_column(String, nullable=False, index=True)
    notes = mapped_column(String)
    music_brainz_id = mapped_column(String)
    last_fm_url = mapped_column(String)

    albums = relationship(
        "Album",
        lazy="dynamic",
        viewonly=True,
        order_by="Album.year.asc(), Album.name.asc()"
    )

    media = relationship(
        "Media",
        lazy="dynamic",
        viewonly=True
    )
