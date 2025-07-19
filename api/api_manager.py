from constants.endpoints import BASE_URL

from api.users_api import UsersAPI


class ApiManager:
    def __init__(self, session, base_url: str = BASE_URL):
        self.session = session
        self.users_api = UsersAPI(session, base_url)
