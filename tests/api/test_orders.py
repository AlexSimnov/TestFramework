import pytest
import allure

from utils.decorators import allure_test_details
from http import HTTPStatus

from db_models.orders import OrderResponse

from constants.messages import ERROR_MESSAGES


@pytest.mark.api
@allure.epic("Тестирование Orders")
@allure.feature("Тестирование Orders routes")
class TestOrders:

    @allure_test_details(
        story="Корректность создания order",
        title="Тест проверки правильности создания order",
        description="""
        Шаги:
        1. Проверяем отсутствие order в БД
        2. Создаем order через API
        3. Проверяем статус код
        4. Проверяем, что ответ — JSON
        5. Проверяем валидность схемы в ответе
        6. Проверяем наличие order в БД
        7. Проверяем, что данные из запроса совпадают с БД
        8. Проверяем, что ответ API соответствует данным в БД
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_post_orders_creates_new_order(
        self,
        db_helper,
        api_manager,
        test_order
    ):

        with allure.step("1. Проверяем отсутствие order в БД"):
            assert db_helper.get_orders_by_user_id(
                test_order.user_id
            ) is False, (
                f"В базе уже присутствует заказ на {test_order.product_name}"
            )

        with allure.step(
            """
            2. Создаем order через API
            3. Проверяем статус код
            4. Проверяем ответ json
            5. Проверяем валидность cхемы в ответе
            """
        ):
            response = api_manager.orders_api.post_orders(
                test_order.model_dump()
                )
            response_json = response.json()
            validated_response = OrderResponse.model_validate(response_json)

        with allure.step("6. Проверяем наличие созданного заказа в БД"):
            assert db_helper.order_exists_by_order_id(
                validated_response.id
            ) is True, "Order не создался в базе"
            order_from_db = db_helper.get_order_by_id(validated_response.id)

        with allure.step(
            "7. Проверяем, что данные из запроса сохранились в БД"
        ):
            assert test_order.user_id == order_from_db.user_id, (
                "user_id не совпадает"
            )
            assert test_order.product_name == order_from_db.product_name, (
                "product_name не совпадает"
                )
            assert test_order.quantity == order_from_db.quantity, (
                "quantity не совпадает"
                )

        with allure.step(
            "8. Проверяем, что ответ API соответствует данным в БД"
        ):
            assert validated_response.user_id == order_from_db.user_id, (
                "user_id не совпадает"
            )
            assert validated_response.product_name == order_from_db.product_name, (
                "product_name не совпадает"
                )
            assert validated_response.quantity == order_from_db.quantity, (
                "quantity не совпадает"
                )

    @allure_test_details(
        story="Корректность создания order",
        title="Тест валидации передаваеммых данных в POST /orders",
        description="""
            Проверка негативных сценариев создания заказа:
            - некорректный quantity
            - невалидный user_id
            - неправильный product_name
            Шаги:
            1. Попытка создать пользователя с не валидным полем
            2. Ожидаем статус код 400
            3. Body - содержание ошибки
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    @pytest.mark.parametrize(
            "invalid_payload, expected_status",
            [
                ({"quantity": 0}, HTTPStatus.BAD_REQUEST),
                ({"quantity": -1}, HTTPStatus.BAD_REQUEST),
                ({"quantity": -50}, HTTPStatus.BAD_REQUEST),
                ({"quantity": 1}, HTTPStatus.CREATED),
                ({"quantity": 99}, HTTPStatus.CREATED),
                ({"quantity": 100}, HTTPStatus.CREATED),
                ({"quantity": 101}, HTTPStatus.BAD_REQUEST),
                ({"quantity": 150}, HTTPStatus.BAD_REQUEST),
                ({"quantity": "abc"}, HTTPStatus.BAD_REQUEST),
                ({"quantity": None}, HTTPStatus.BAD_REQUEST),
                ({"quantity": ""}, HTTPStatus.BAD_REQUEST),
                ({"quantity": "1"}, HTTPStatus.BAD_REQUEST),
                ({"quantity": "True"}, HTTPStatus.BAD_REQUEST),
                ({"quantity": True}, HTTPStatus.BAD_REQUEST),
                ({"quantity": 1.23}, HTTPStatus.BAD_REQUEST),
                ({"quantity": "1.23"}, HTTPStatus.BAD_REQUEST),

                ({"user_id": 999999}, HTTPStatus.BAD_REQUEST),
                ({"user_id": 0}, HTTPStatus.BAD_REQUEST),
                ({"user_id": "abc"}, HTTPStatus.BAD_REQUEST),
                ({}, HTTPStatus.BAD_REQUEST),

                ({"product_name": ""}, HTTPStatus.BAD_REQUEST),
                ({"product_name": "   "}, HTTPStatus.BAD_REQUEST),
                ({"product_name": "X" * 300}, HTTPStatus.BAD_REQUEST),
                ({"product_name": "Laptop"}, HTTPStatus.CREATED),
                ({}, HTTPStatus.BAD_REQUEST),
            ]
    )
    def test_orders_create_negative(
        api_manager,
        test_order,
        invalid_payload,
        expected_status
    ):
        order_payload = test_order.model_dump()

        order_payload.update(invalid_payload)

        with allure.step(
            "1. Попытка создать заказ с некорректными данными: {}".format(
                invalid_payload
            ),
            "2. Ожидаем статус код 400"
        ):
            response = api_manager.orders_api.post_orders(
                data=order_payload,
                expected_status=expected_status
            )
            response_json = response.json()

        with allure.step(
            "3. Проверка, что возвращено корректное сообщение об ошибке"
        ):
            assert response_json == ERROR_MESSAGES.BAD_REQUEST

    @allure_test_details(
        story="Корректность создания order",
        title="Тест повторного создания с теми же данными",
        description="""
        Шаги:
        1. Создание первого заказа через API
        2. Проверка, что заказ создан
        3. Проверка наличия первого заказа в БД
        4. Повторная отправка такого же заказа
        5. Проверка, что создан второй заказ
        6. Проверка, что в БД два заказа с одинаковыми данными
        """,
        severity=allure.severity_level.CRITICAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_orders_create_duplicates(api_manager, db_helper, test_order):
        payload = test_order.model_dump()

        with allure.step("1. Создание первого заказа"):
            first_order_resp = api_manager.orders_api.post_orders(
                data=payload,
                expected_status=HTTPStatus.CREATED
            )
            first_order_resp_json = first_order_resp.json()
            validated_order1 = OrderResponse.model_validate(
                first_order_resp_json
                )

        with allure.step("2. Проверка валидности первого ответа"):
            assert validated_order1.product_name == payload["product_name"]
            assert validated_order1.quantity == payload["quantity"]
            assert validated_order1.user_id == payload["user_id"]

        with allure.step("3. Проверка наличия первого заказа в БД"):
            assert db_helper.order_exists_by_user_id(
                payload["user_id"]
            ) is True, "Первый заказ не найден в БД"

        with allure.step(
            "4. Повторная попытка создать заказ с теми же данными"
        ):
            second_order_resp = api_manager.orders_api.post_orders(
                data=payload,
                expected_status=HTTPStatus.CREATED
            )
            second_order_resp_json = second_order_resp.json()
            validated_order2 = OrderResponse.model_validate(
                second_order_resp_json
                )

        with allure.step("5. Проверка, что второй заказ также успешно создан"):
            assert validated_order2.id != validated_order1.id, (
                "ID заказов должны отличаться"
            )
            assert validated_order2.product_name == payload["product_name"]

        with allure.step(
            "6. Проверка, что в БД два заказа с одинаковыми данными"
        ):
            orders = db_helper.get_orders_by_user_id(payload["user_id"])
            assert orders.count() == 2, (
                f"Ожидалось 2 заказа, найдено: {orders.count()}"
            )

    @allure_test_details(
        story="Корректность получения order по id",
        title="Тест проверки получения заказа по существующему order_id",
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
    def test_get_order_by_id(api_manager, create_order):

        with allure.step("1. Получение заказа по его ID"):
            response = api_manager.orders_api.get_order_by_id(
                order_id=create_order.id,
                expected_status=HTTPStatus.OK
            )
            response_json = response.json()
            fetched_order = OrderResponse.model_validate(response_json)

        with allure.step("2. Проверка, что возвращен статус 200 OK"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("3. Валидация структуры и типов полей"):
            assert isinstance(fetched_order.id, int)
            assert isinstance(fetched_order.user_id, int)
            assert isinstance(fetched_order.product_name, str)
            assert isinstance(fetched_order.quantity, int)

        with allure.step(
            """
            5. Проверка, что возвращённые данные совпадают с созданным заказом
            """
        ):
            assert fetched_order.id == create_order.id
            assert fetched_order.user_id == create_order.user_id
            assert fetched_order.product_name == create_order.product_name
            assert fetched_order.quantity == create_order.quantity

    @pytest.mark.parametrize(
        "order_id_input, expected_status",
        [
            (0, HTTPStatus.NOT_FOUND),
            (-1, HTTPStatus.NOT_FOUND),
            (999999, HTTPStatus.NOT_FOUND),
            ("abc", HTTPStatus.NOT_FOUND),
            (None, HTTPStatus.NOT_FOUND),
            (1.5, HTTPStatus.NOT_FOUND),
        ]
    )
    @allure_test_details(
        story="Получение order по невалидному или несуществующему ID",
        title="Тест негативных сценариев получения orders",
        description="""
            Шаги:
            1. GET запрос с невалидным или несуществующим ID
            2. Проверка, что API возвращает корректный статус ошибки
        """,
        severity=allure.severity_level.NORMAL,
        label=("qa_name", "Simonov Aleksei"),
    )
    def test_get_order_by_invalid_id(
        api_manager,
        invalid_order_id,
        expected_status
    ):
        with allure.step(
            "1. GET запрос с невалидным или несуществующим ID"
            "2. Проверка, что API возвращает корректный статус ошибки"
        ):
            response = api_manager.orders_api.get_order_by_id(
                order_id=invalid_order_id,
                expected_status=expected_status
            )
            response = response.json()
