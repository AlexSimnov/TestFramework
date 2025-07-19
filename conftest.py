import pytest
import requests

from api.api_manager import ApiManager

from db_requester.db_client import get_db_session

from db_requester.db_helpers import DBHelper


@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture(scope='class')
def api_manager():
    """
    Фикстура для создания экземпляра ApiManager
    """

    session = requests.Session()

    yield ApiManager(session)

    session.close()


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
