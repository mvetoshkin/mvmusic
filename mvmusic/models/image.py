from sqlalchemy import Column, String
from mvmusic.models import BaseModel


class Image(BaseModel):
    path = Column(String, nullable=False)
