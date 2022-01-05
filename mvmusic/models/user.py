import bcrypt
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship, validates

from . import BaseModel


class User(BaseModel):
    username = Column(String(128), nullable=False, unique=True, index=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    libraries = relationship(
        'Library',
        secondary='user_library',
        lazy='joined',
        order_by='Library.name'
    )

    # noinspection PyUnusedLocal
    @validates('password')
    def validate_password(self, key, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()

    def passwords_matched(self, password):
        if not self.password:
            return False
        return bcrypt.checkpw(password.encode(), self.password.encode())
