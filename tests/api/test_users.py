import pytest
import allure

from utils.decorators import allure_test_details
from constants.messages import ERROR_MESSAGES

from models.users_models import UserResponce

from http import HTTPStatus

from utils.data_generator import UserDataGenerator


@pytest.mark.api
@allure.epic("Тестирование Users")
@allure.feature("Тестирование Users routes")
class TestUsers:

    @allure_test_details(
        story="Корректность создания user",
        title=(
            "Тест проверки правильности создания user"
        ),
        description="""
        Шаги:
        1. Проверяем отсутствие пользоваетеля в бд
        2. Создаем пользователя с кредами через api
        3. Проверяем статус код
        4. Проверяем ответ = json
        5. Проверяем валидность cхемы в ответе
        6. Проверяем создание уникального пользователя в бд
        7. Проверяем, что данные из запроса сохранились в БД"
        8. Проверяем, что ответ API соответствует данным в БД
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_users_create_valid(self, db_helper, api_manager, test_user):

        with allure.step("1. Проверяем отсутствие пользоваетеля в бд"):
            assert db_helper.user_exists_by_username(
                test_user.username) is False, (
                "В базе уже присутствует user "
                f"c username: {test_user.username}"
            )

        with allure.step(
            """
            2. Создаем пользователя с кредами
            3. Проверяем статус код
            4. Проверяем ответ json
            5. Проверяем валидность cхемы в ответе
            """
        ):
            responce = api_manager.users_api.post_users(test_user.model_dump())
            responce = responce.json()
            responce = UserResponce.model_validate(responce)

        with allure.step(
            "6. Проверяем создание уникального пользователя в бд"
        ):

            assert db_helper.user_exists_by_username(
                test_user.username) is True, (
                f"В базе user c {test_user.username} не уникален"
            )
            user_from_db = db_helper.get_user_by_username(test_user.username)

        with allure.step(
            "7. Проверяем, что данные из запроса сохранились в БД"
        ):
            assert test_user.username == user_from_db.username, (
                f"Ожидалось имя {test_user.username},"
                f"получено {user_from_db.username}"
            )
            assert test_user.email == user_from_db.email, (
                f"Ожидалось email {test_user.email},"
                f"получено {user_from_db.email}"
            )
            assert test_user.age == user_from_db.age, (
                f"Ожидалось email {test_user.age},"
                f"получено {user_from_db.age}"
            )

        with allure.step(
            "8. Проверяем, что ответ API соответствует данным в БД"
        ):
            assert responce.username == user_from_db.username, (
                f"Ожидалось имя {test_user.username},"
                f"получено {user_from_db.username}"
            )
            assert responce.email == user_from_db.email, (
                f"Ожидалось email {test_user.email},"
                f"получено {user_from_db.email}"
            )
            assert responce.age == user_from_db.age, (
                f"Ожидалось email {test_user.age},"
                f"получено {user_from_db.age}"
            )

    @pytest.mark.parametrize(
        "field, value, expected_status",
        [
            ("username", "ab", HTTPStatus.BAD_REQUEST),
            ("username", "a b c", HTTPStatus.BAD_REQUEST),
            ("username", "", HTTPStatus.BAD_REQUEST),
            ("username", None, HTTPStatus.BAD_REQUEST),
            ("username", 1, HTTPStatus.BAD_REQUEST),
            ("username", "1", HTTPStatus.BAD_REQUEST),
            ("username", "True", HTTPStatus.BAD_REQUEST),
            ("username", True, HTTPStatus.BAD_REQUEST),
            ("username", 1.23, HTTPStatus.BAD_REQUEST),
            ("username", "1.23", HTTPStatus.BAD_REQUEST),

            ("email", "", HTTPStatus.BAD_REQUEST),
            ("email", "a b c", HTTPStatus.BAD_REQUEST),
            ("email", "a b c@gmail.com", HTTPStatus.BAD_REQUEST),
            ("email", None, HTTPStatus.BAD_REQUEST),
            ("email", 1, HTTPStatus.BAD_REQUEST),
            ("email", "1", HTTPStatus.BAD_REQUEST),
            ("email", "True", HTTPStatus.BAD_REQUEST),
            ("email", True, HTTPStatus.BAD_REQUEST),
            ("email", 1.23, HTTPStatus.BAD_REQUEST),
            ("email", "1.23", HTTPStatus.BAD_REQUEST),

            ("age", 0, HTTPStatus.BAD_REQUEST),
            ("age", -10, HTTPStatus.BAD_REQUEST),
            ("age", 100, HTTPStatus.BAD_REQUEST),
            ("age", 130, HTTPStatus.BAD_REQUEST),
            ("age", "abc", HTTPStatus.BAD_REQUEST),
            ("age", "a", HTTPStatus.BAD_REQUEST),
            ("age", "", HTTPStatus.BAD_REQUEST),
            ("age", None, HTTPStatus.BAD_REQUEST),
            ("age", "1", HTTPStatus.BAD_REQUEST),
            ("age", "True", HTTPStatus.BAD_REQUEST),
            ("age", True, HTTPStatus.BAD_REQUEST),
            ("age", 1.23, HTTPStatus.BAD_REQUEST),
            ("age", "1.23", HTTPStatus.BAD_REQUEST),
            ("age", "Киря12", HTTPStatus.BAD_REQUEST),

            ("username", "abc", HTTPStatus.CREATED),
            ("email", "valid@example.com", HTTPStatus.CREATED),
            ("age", 25, HTTPStatus.CREATED),
        ]
    )
    @allure_test_details(
        story="Корректность создания user",
        title="Тест проверки валидации одного из полей (username, email, age)",
        description="""
        Шаги:
        1. Попытка создать пользователя с не валидным полем
        2. Ожидаем статус код 400
        3. Body - содержание ошибки
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_user_create_field_validation(api_manager,
                                          test_user,
                                          field,
                                          value,
                                          expected_status):
        payload = test_user.model_dump()
        payload[field] = value

        with allure.step(
            "1. Попытка создать пользователя с не валидным полем"
            "2. Ожидаем статус код 400"
        ):
            response = api_manager.users_api.post_users(
                data=payload,
                expected_status=expected_status
            )
            response_json = response.json()

        with allure.step("3. Body - содержание ошибки"):
            assert response_json == ERROR_MESSAGES.BAD_REQUEST

    @allure_test_details(
        story="Корректность создания user",
        title=(
            "Тест проверки, что username уникален"
        ),
        description="""
        Шаги:
        1. Попытка создать user с такими же username которые в БД
        2. Ожидаем ошибку, что уже есть такой user c username
        3. Проверка что user с такими username не создался в БД
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_users_create_unique_username(self,
                                          api_manager,
                                          setup_user_db,
                                          db_helper):
        created_user = setup_user_db
        user_payload = {
            "username": created_user.username,
            "email": UserDataGenerator.generate_random_email(),
            "age": created_user.age,
        }
        with allure.step(
            "1. Попытка создать user с такими же username которые в БД"
        ):
            responce = api_manager.users_api.post_users(
                data=user_payload,
                expected_status=HTTPStatus.CONFLICT
                )
            responce = responce.json()

        with allure.step(
            "2. Ожидаем ошибку, что уже есть такой user c username"
        ):
            assert responce == ERROR_MESSAGES.NON_UNIQUE_FIELD, (
                "В базе уже присутствует c таким username"
            )

        with allure.step(
            "3. Проверка что user с такими username не создался в БД"
        ):
            assert db_helper.user_exists_by_username(
                created_user.username
            ) == 1, (
                "В базе уже присутствует user "
                "c username: {}".format(
                    created_user.username
                )
            )

    @allure_test_details(
        story="Корректность создания user",
        title=(
            "Тест проверки, что email уникален"
        ),
        description="""
        Шаги:
        1. Попытка создать user с такими же email которые в БД
        2. Ожидаем ошибку, что уже есть такой user c email
        3. Проверка что user с такими email не создался в БД
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_users_create_unique_email(self,
                                       api_manager,
                                       setup_user_db,
                                       db_helper):
        created_user = setup_user_db
        user_payload = {
            "username": UserDataGenerator.generate_random_username,
            "email": created_user.email,
            "age": created_user.age,
        }
        with allure.step(
            "1. Попытка создать user с такими же email которые в БД"
        ):
            responce = api_manager.users_api.post_users(
                data=user_payload,
                expected_status=HTTPStatus.CONFLICT
                )
            responce = responce.json()

        with allure.step(
            "2. Ожидаем ошибку, что уже есть такой user c email"
        ):
            assert responce == ERROR_MESSAGES.NON_UNIQUE_FIELD, (
                "В базе уже присутствует c таким email"
            )

        with allure.step(
            "3. Проверка что user с такими email не создался в БД"
        ):
            assert db_helper.user_exists_by_username(
                created_user.username
            ) == 1, (
                "В базе уже присутствует user "
                "c email: {}".format(
                    created_user.email
                )
            )

    @allure_test_details(
        story="Корректность получения user",
        title=(
            "Тест проверки корректности отданных данных user"
        ),
        description="""
        Шаги:
        1. Получение user через api по id
        2. Проревяряем статус код
        3. Проверяем ответ = json
        4. Проверяем валидность схемы
        5. Проверяем, что ответ API соответствует данным в БД
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_users_get_valid(self, api_manager, setup_user_db):
        created_user = setup_user_db

        with allure.step(
            """
            1. Получение user через api по {}
            2. Проревяряем статус код
            3. Проверяем ответ = json
            4. Проверяем валидность схемы
            """.format(created_user.id)
        ):
            responce = api_manager.users_api.get_users_by_id(created_user.id)
            responce = responce.json()
            responce = UserResponce.model_validate(responce)

        with allure.step(
            "5. Проверяем, что ответ API соответствует данным в БД"
        ):
            assert created_user.id == responce.id, (
                "Id не совпадает"
            )
            assert created_user.username == responce.username, (
                "Username не совпадает"
            )
            assert created_user.email == responce.email, (
                "Email не совпадает"
            )
            assert created_user.age == responce.age, (
                "Age не совпадает"
            )

    @pytest.mark.parametrize(
        "invalid_id_param, expected_status",
        [
            "a",
            "",
            None,
            2,
            "2",
            "True",
            True,
            1.23,
            "1.23"
            - 1,
            0,
            9999999
        ]
    )
    @allure_test_details(
        story="Корректность получения user",
        title=(
            "Получение user по невалидному или несуществующему ID"
        ),
        description="""
        Шаги:
        1. Получение user через api по type != id
        2. Ожидаем ошибку 404
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_users_get_invalid_id(self,
                                  api_manager,
                                  setup_user_db,
                                  invalid_id_param):

        with allure.step(
            "1. Получение user через api по != id"
            "2. Ожидаем ошибку 404"
        ):
            responce = api_manager.users_api.get_users_by_id(
                id=invalid_id_param,
                expected_status=HTTPStatus.NOT_FOUND
            )
            responce = responce.json()
