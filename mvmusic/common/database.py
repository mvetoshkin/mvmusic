from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from mvmusic.common.utils import settings


class DB:
    __instance = None
    session = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DB, cls).__new__(cls)

            engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
            cls.__instance.session = scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=engine)
            )

        return cls.__instance
