import pytest

from schemas.users import UserDBModel
from schemas.orders import OrderDBModel

from utils.data_generator import OrderGenerator, UserDataGenerator


@pytest.fixture
def test_user():
    """
    Генерация данных для нового user
    """
    return UserDataGenerator.generate_user_payload()


@pytest.fixture
def setup_user_db(db_session, test_user):
    """
    Создание тестового пользователя в БД
    """
    test_user_db = UserDBModel(
        username=test_user.username,
        email=test_user.email,
        age=test_user.age
    )
    db_session.add(test_user_db)
    db_session.commit()
    yield db_session, test_user_db
    db_session.delete(test_user_db)
    db_session.commit()


@pytest.fixture
def test_order(setup_user_db):
    """
    Генерация данных для order
    """
    _, created_user = setup_user_db
    return OrderGenerator.generate_order_payload(created_user.id)


@pytest.fixture
def create_order(test_order):
    """
    Создание нового заказа
    """
    db_session, test_order = test_order
    test_order_db = OrderDBModel(
        user_id=test_order.user_id,
        product_name=test_order.product_name,
        quantity=test_order.quantity
    )
    db_session.add(test_order_db)
    db_session.commit()
    return test_order_db
