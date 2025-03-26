from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import mapped_column, relationship

from mvmusic.models import BaseModel


class Client(BaseModel):
    name = mapped_column(String, nullable=False)

    user_id = mapped_column(
        String,
        ForeignKey("user.id", ondelete="cascade"),
        index=True,
        nullable=False
    )

    user = relationship("User", innerjoin=True, uselist=False)


Index(
    "ix_client_name_user_id",
    Client.name,
    Client.user_id,
    unique=True
)
