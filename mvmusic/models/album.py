from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, ImageMixin, ScannedMixin


class Album(ImageMixin, ScannedMixin, BaseModel):
    name = mapped_column(String, nullable=False, index=True)
    year = mapped_column(Integer)
    notes = mapped_column(String)
    music_brainz_id = mapped_column(String)
    last_fm_url = mapped_column(String)

    artist_id = mapped_column(
        String,
        ForeignKey("artist.id", ondelete="cascade"),
        nullable=False
    )

    artist = relationship(
        "Artist",
        uselist=False,
        lazy="joined"
    )

    media = relationship(
        "Media",
        lazy="dynamic",
        viewonly=True,
        order_by="Media.disc_number.asc(), Media.track.asc(), Media.title.asc()"
    )
