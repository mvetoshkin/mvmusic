from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from mvmusic.settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = scoped_session(sessionmaker(autocommit=False, bind=engine))
