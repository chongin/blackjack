from api_clients.api_client_base import ApiClientBase


class Authorization(ApiClientBase):
    def __init__(self, endpoint='https://www.mock_authorization.com', timeout=10) -> None:
        super().__init__(endpoint, timeout)

    def login(self, player_info: dict) -> bool:
        return True

    def logout(self, player_info: dict) -> bool:
        return True
    