import re
from datetime import datetime
from uuid import uuid4

import shortuuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Query

from mvmusic.common.database import db


class BaseQuery(Query):
    pass


class BaseModel(declarative_base()):
    __abstract__ = True

    name_prefix = None
    query = db.session.query_property(query_cls=BaseQuery)

    id_ = Column(
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
