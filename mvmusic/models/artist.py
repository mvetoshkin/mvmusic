from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Artist(BaseModel):
    name = mapped_column(String, index=True, nullable=False)
    scanned = mapped_column(Boolean, default=False, nullable=False)

    last_fm_url = mapped_column(String)
    music_brainz_id = mapped_column(String)
    notes = mapped_column(String)

    image_id = mapped_column(
        String,
        ForeignKey("image.id", ondelete="set null"),
        index=True
    )

    albums = relationship("Album", order_by="Album.year", viewonly=True)
    image = relationship("Image", uselist=False)
    media = relationship("Media", order_by="Media.title", viewonly=True)
