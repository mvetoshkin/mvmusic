from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from mvmusic.models import BaseModel


class Image(BaseModel):
    path = mapped_column(String, nullable=False, unique=True)
    mimetype = mapped_column(String, nullable=False)
    height = mapped_column(Integer, nullable=False)
    width = mapped_column(Integer, nullable=False)
