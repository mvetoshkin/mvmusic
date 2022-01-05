from sqlalchemy.orm import relationship

from mvmusic.models import BaseModel, ImageModel, PathModel


class Directory(BaseModel, PathModel, ImageModel):
    children = relationship(
        'Directory',
        lazy='dynamic',
        viewonly=True,
        order_by='Directory.path.asc()'
    )

    media = relationship(
        'Media',
        lazy='dynamic',
        viewonly=True,
        order_by='Media.track.asc(), Media.title.asc()'
    )

    @property
    def name(self):
        return self.path.rpartition('/')[-1]
