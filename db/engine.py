from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants.config import (
    USERNAME_DB,
    PASSWORD_DB,
    HOST_DB,
    PORT_DB,
    DATABASE_NAME_DB
)


engine = create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(
        USERNAME_DB,
        PASSWORD_DB,
        HOST_DB,
        PORT_DB,
        DATABASE_NAME_DB)
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
