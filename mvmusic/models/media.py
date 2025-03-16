from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel, ImageMixin, PathMixin, ScannedMixin


class Media(PathMixin, ImageMixin, ScannedMixin, BaseModel):
    title = mapped_column(String)
    year = mapped_column(Integer)
    track = mapped_column(Integer)
    disc_number = mapped_column(Integer)
    duration = mapped_column(Integer)
    bitrate = mapped_column(Integer)
    size = mapped_column(Integer)
    content_type = mapped_column(String)
    is_video = mapped_column(Boolean)

    album_id = mapped_column(
        String,
        ForeignKey("album.id", ondelete="cascade")
    )

    artist_id = mapped_column(
        String,
        ForeignKey("artist.id", ondelete="cascade")
    )

    album = relationship(
        "Album",
        uselist=False,
        lazy="joined"
    )

    artist = relationship(
        "Artist",
        uselist=False,
        lazy="joined"
    )

    genres = relationship(
        "Genre",
        secondary="media_genre",
        lazy="joined"
    )
