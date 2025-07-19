import random
import logging
import string
from faker import Faker

from models.users_models import UserCreate
from models.orders_models import OrderCreate

from constants.products import PRODUCTS

faker = Faker("ru_RU")
logger = logging.getLogger(__name__)


class UserDataGenerator:

    @staticmethod
    def generate_user_payload() -> UserCreate:
        """
        Генерация рандомных кредов для user
        """
        user_data = UserCreate(
            username=UserDataGenerator.generate_random_name(),
            email=UserDataGenerator.generate_random_email(),
            age=UserDataGenerator.generate_random_age()
        )
        logger.debug(
            f"""Сгенерированы данные для создания пользователя:
                Email - {user_data.email}"""
            )
        return user_data

    @staticmethod
    def generate_random_email():
        """
        Генерация рандомного email
        """
        return faker.safe_email()

    @staticmethod
    def generate_random_username(strings: int = 8):
        """
        Генерация рандомного имени
        """
        first_name = "".join(random.choices(string.ascii_lowercase, k=strings))
        return f"{first_name.capitalize()}"

    @staticmethod
    def generate_random_age(min_age: int = 1, max_age: int = 100):
        """
        Генерация рандомного возраста
        """
        return random.randint(min_age, max_age)


class OrderGenerator:

    @staticmethod
    def generate_order_payload(user_id: int) -> OrderCreate:
        """
        Генерация рандомного order у user_id
        """
        order_data = OrderCreate(
            user_id=user_id,
            product_name=OrderGenerator.generate_random_product(),
            quantity=OrderGenerator.generate_random_quantity()
        )
        logger.debug(
            f"""Сгенерированы данные для создания order:
                User_id - {user_id}"""
            )
        return order_data

    @staticmethod
    def generate_random_quantity(
        min_quantity: int = 1,
        max_quantity: int = 100
    ):
        """
        Генерация рандомного quantity
        """
        return random.randint(min_quantity, max_quantity)

    @staticmethod
    def generate_random_product(strings: int = 8):
        """
        Генерация рандомного имени
        """
        return f"{random.choice(PRODUCTS)}"
