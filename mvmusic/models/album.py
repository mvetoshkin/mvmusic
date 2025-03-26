from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Album(BaseModel):
    name = mapped_column(String, nullable=False)
    scanned = mapped_column(Boolean, default=False, nullable=False)

    last_fm_url = mapped_column(String)
    music_brainz_id = mapped_column(String)
    notes = mapped_column(String)
    year = mapped_column(Integer)

    artist_id = mapped_column(
        String,
        ForeignKey("artist.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    image_id = mapped_column(
        String,
        ForeignKey("image.id", ondelete="set null"),
        index=True
    )

    artist = relationship("Artist", innerjoin=True, uselist=False)
    image = relationship("Image", uselist=False)
    media = relationship(
        "Media",
        innerjoin=True,
        order_by="Media.track, Media.title",
        viewonly=True
    )


Index(
    "ix_album_name_year_artist_id",
    Album.name,
    Album.year,
    Album.artist_id,
    unique=True
)
