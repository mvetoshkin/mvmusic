import re
from datetime import datetime
from uuid import uuid4

import shortuuid
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Query, relationship

from mvmusic.common.database import db
from mvmusic.common.decorators import get_one
from mvmusic.common.exceptions import NotFoundError


class BaseQuery(Query):
    def get(self, ident):
        obj = super(BaseQuery, self).get(ident)
        if not obj:
            raise NotFoundError
        return obj

    @get_one
    def get_by(self, **kwargs):
        return self.filter_by(**kwargs)


class BaseModel(declarative_base()):
    __abstract__ = True

    name_prefix = None
    query = db.session.query_property(query_cls=BaseQuery)

    id_: Column = Column(
        'id',
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    created_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    modified_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id_}>'

    @declared_attr
    def __tablename__(self):
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', self.__name__).lower()
        if self.name_prefix:
            name = self.name_prefix + '_' + name
        return name

    @property
    def short_id(self):
        return shortuuid.encode(self.id_)

    @classmethod
    def create(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        db.session.add(obj)
        db.session.flush()
        return obj

    def delete(self):
        db.session.delete(self)
        db.session.flush()


class PathModel:
    path = Column(String, nullable=False, index=True)
    last_seen = Column(DateTime)

    @declared_attr
    def library_id(self) -> Column:
        return Column(
            String,
            ForeignKey('library.id', ondelete='cascade'),
            nullable=False
        )

    @declared_attr
    def parent_id(self) -> Column:
        return Column(
            String,
            ForeignKey('directory.id', ondelete='cascade')
        )

    @declared_attr
    def library(self):
        return relationship(
            'Library',
            lazy='joined',
            uselist=False
        )

    @declared_attr
    def parent(self):
        return relationship(
            'Directory',
            lazy='joined',
            uselist=False,
            remote_side='Directory.id_'
        )


class ImageModel:
    @declared_attr
    def image_id(self):
        return Column(
            String,
            ForeignKey('image.id', ondelete='set null')
        )

    @declared_attr
    def image(self):
        return relationship(
            'Image',
            lazy='joined',
            uselist=False
        )
