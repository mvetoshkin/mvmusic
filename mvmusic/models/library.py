from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from mvmusic.models import BaseModel


class Library(BaseModel):
    name = mapped_column(String, nullable=False, unique=True)
    path = mapped_column(String, nullable=False, unique=True)
