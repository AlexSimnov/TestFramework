from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderDBModel(Base):
    __tablename__ = 'order'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False)
    product_name: str = Column(String(100), nullable=False)
    quantity: int = Column(Integer(100), nullable=False)
