from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from typing import Any, Dict

Base = declarative_base()


class OrderDBModel(Base):
    __tablename__ = 'orders'

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False)
    product_name: str = Column(String(100), nullable=False)
    quantity: int = Column(Integer, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование заказа в словарь
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
        }

    def __repr__(self):
        return (
            f"<Order(id={self.id}, user_id={self.user_id}, "
            f"product_name='{self.product_name}', quantity={self.quantity})>"
        )
