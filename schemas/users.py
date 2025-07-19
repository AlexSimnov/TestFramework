from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserDBModel(Base):
    __tablename__ = 'user'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), nullable=False)
    email: str = Column(String(100), nullable=False, unique=True)
    age: int = Column(Integer)
