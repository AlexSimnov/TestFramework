from sqlalchemy.orm import Session
from db_models.users import UserDBModel
from db_models.orders import OrderDBModel


class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    """Класс с методами для работы с БД в тестах"""

    # USER
    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: str):
        """Получает пользователя по ID"""
        return self.db_session.query(UserDBModel).filter(
            UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Получает пользователя по email"""
        return self.db_session.query(UserDBModel).filter(
            UserDBModel.email == email).first()

    def get_user_by_username(self, username: str):
        """Получает пользователя по username"""
        return self.db_session.query(UserDBModel).filter(
            UserDBModel.email == username).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return self.db_session.query(UserDBModel).filter(
            UserDBModel.email == email).count() > 0

    def user_exists_by_username(self, username: str) -> bool:
        """Проверяет существование пользователя по username"""
        return self.db_session.query(UserDBModel).filter(
            UserDBModel.username == username).count() > 0

    def delete_user(self, user: UserDBModel):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    # ORDER
    def create_test_order(self, order_data: dict) -> OrderDBModel:
        """Создаёт тестовый заказ"""
        order = OrderDBModel(**order_data)
        self.db_session.add(order)
        self.db_session.commit()
        self.db_session.refresh(order)
        return order

    def get_order_by_id(self, order_id: int) -> OrderDBModel:
        """Получает заказ по ID"""
        return self.db_session.query(OrderDBModel).filter(
            OrderDBModel.id == order_id
        ).first()

    def get_orders_by_user_id(self, user_id: int) -> list[OrderDBModel]:
        """Получает все заказы пользователя"""
        return self.db_session.query(OrderDBModel).filter(
            OrderDBModel.user_id == user_id
        ).all()

    def order_exists_by_order_id(self, order_id: int) -> bool:
        """Проверяет существование заказа по order_id"""
        return self.db_session.query(OrderDBModel).filter(
            OrderDBModel.user_id == order_id).count() > 0

    def order_exists_by_user_id(self, user_id: int) -> bool:
        """Проверяет существование заказа по user_id"""
        return self.db_session.query(OrderDBModel).filter(
            OrderDBModel.user_id == user_id).count() > 0

    def delete_order(self, order: OrderDBModel):
        """Удаляет заказ"""
        self.db_session.delete(order)
        self.db_session.commit()
