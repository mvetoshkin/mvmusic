import re
from datetime import datetime
from uuid import uuid4

import shortuuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Query
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from mvmusic.common.database import DB
from mvmusic.common.utils import classproperty


class BaseQuery(Query):
    pass


class BaseModel(declarative_base()):
    __abstract__ = True

    name_prefix = None

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
        name = f'<{self.__class__.__name__} {self.id_}>'
        if self.name_prefix:
            name = self.name_prefix + '_' + name

        return name

    @declared_attr
    def __tablename__(self):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__name__).lower()

    @classproperty
    def query(self):
        return DB().session.query(self)

    @property
    def short_id(self):
        return shortuuid.encode(self.id_)
