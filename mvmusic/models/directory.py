from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, PathModel


class Directory(BaseModel, PathModel):
    children = relationship('Directory', lazy='dynamic', viewonly=True)
    media = relationship('Media', lazy='dynamic', viewonly=True)

    @property
    def name(self):
        return self.path.rpartition('/')[-1]
