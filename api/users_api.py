from custom_requester.custom_requester import CustomRequester

from constants.endpoints import USERS_ENDPOINT


class UsersAPI(CustomRequester):
    """
    Класс для работы API Users
    """

    def __init__(self, session, base_url):
        super().__init__(session, base_url)

    def post_users(self, data, expected_status=201):
        """
        Создание нового пользователя
        """
        return self.send_request(
            method="POST",
            endpoint=USERS_ENDPOINT,
            data=data,
            expected_status=expected_status
        )

    def get_users_by_id(self, id, expected_status=200):
        """
        Получение о пользователе по id
        """
        return self.send_request(
            method="GET",
            endpoint=f"{USERS_ENDPOINT}/{id}",
            expected_status=expected_status
        )
