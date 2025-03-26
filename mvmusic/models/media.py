from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Media(BaseModel):
    last_seen = mapped_column(DateTime, index=True, nullable=False)
    path = mapped_column(String, nullable=False, unique=True)
    scanned = mapped_column(Boolean, default=False, nullable=False)

    bitrate = mapped_column(Integer)
    content_type = mapped_column(String)
    disc_number = mapped_column(Integer)
    duration = mapped_column(Integer)
    is_video = mapped_column(Boolean)
    size = mapped_column(Integer)
    title = mapped_column(String)
    track = mapped_column(Integer)
    year = mapped_column(Integer)

    album_id = mapped_column(
        String,
        ForeignKey("album.id", ondelete="cascade"),
        index=True
    )

    artist_id = mapped_column(
        String,
        ForeignKey("artist.id", ondelete="cascade"),
        index=True
    )

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
        index=True,
        nullable=False
    )

    album = relationship("Album", uselist=False)
    artist = relationship("Artist", uselist=False)
    genres = relationship("Genre", secondary="media_genre")
    image = relationship("Image", uselist=False)
    library = relationship("Library", innerjoin=True, uselist=False)
    parent = relationship("Directory", innerjoin=True, uselist=False)


Index(
    "ix_media_library_id_path",
    Media.library_id,
    Media.path,
    unique=True
)


Index(
    "ix_media_id_library_id",
    Media.id,
    Media.library_id,
    unique=True
)
