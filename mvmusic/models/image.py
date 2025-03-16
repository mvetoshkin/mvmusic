from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from mvmusic.models import BaseModel


class Image(BaseModel):
    path = mapped_column(String, nullable=False)
    mimetype = mapped_column(String)
    height = mapped_column(Integer)
    width = mapped_column(Integer)
