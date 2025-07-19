from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from typing import Any, Dict

Base = declarative_base()


class UserDBModel(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), nullable=False)
    email: str = Column(String(100), nullable=False, unique=True)
    age: int = Column(Integer)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование в словарь
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "age": self.age,
        }

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}')>"
