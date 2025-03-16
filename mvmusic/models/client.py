from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from mvmusic.models import BaseModel, UserMixin


class Client(UserMixin, BaseModel):
    name = mapped_column(String, nullable=False, index=True)
