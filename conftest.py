import pytest
import requests

from api.api_manager import ApiManager

from db.engine import SessionLocal


@pytest.fixture(scope='class')
def api_manager():
    """Фикстура для создания экземпляра ApiManager"""

    session = requests.Session()

    yield ApiManager(session)

    session.close()


@pytest.fixture(autouse=True)
def db_session():
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных.
    После завершения теста сессия автоматически закрывается.
    """
    db_session = SessionLocal()
    trans = db_session.begin()
    yield db_session
    trans.rollback()
    db_session.close()


@pytest.fixture
def user_session():
    """
    Создание пула сессий для users
    Закрываются автоматически когда завершается прогон
    """
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()
