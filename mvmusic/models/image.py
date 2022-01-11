from sqlalchemy import Column, String, Integer
from mvmusic.models import BaseModel


class Image(BaseModel):
    path = Column(String, nullable=False)
    mimetype = Column(String)
    height = Column(Integer)
    width = Column(Integer)
