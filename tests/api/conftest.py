import pytest

from utils.data_generator import OrderGenerator, UserDataGenerator


@pytest.fixture
def test_user():
    """
    Генерация данных для нового user
    """
    return UserDataGenerator.generate_user_payload()


@pytest.fixture
def setup_user_db(db_helper, test_user):
    """
    Создание тестового пользователя в БД
    """
    user = db_helper.create_test_user(test_user.model_dump())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


@pytest.fixture
def test_order(setup_user_db):
    """
    Генерация данных для order
    """
    created_user = setup_user_db
    return OrderGenerator.generate_order_payload(created_user.id)


@pytest.fixture
def create_order(test_order, db_helper):
    """
    Создание нового заказа
    """
    order = db_helper.create_test_order(test_order.model_dump())
    yield order
    if db_helper.get_user_by_id(order.id):
        db_helper.delete_user(order)
