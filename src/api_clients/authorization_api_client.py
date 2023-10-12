from api_clients.api_client_base import ApiClientBase


class AuthorizationApiClient(ApiClientBase):
    def __init__(self, endpoint='https://www.mock_authorization.com', timeout=10) -> None:
        super().__init__(endpoint, timeout)

    def validate_player(self, player_info) -> bool:
        print("AuthorizationApi validate_player call.")
        return True
    
    def login(self, player_info: dict) -> bool:
        print("AuthorizationApi login call.")
        return True

    def logout(self, player_info: dict) -> bool:
        print("AuthorizationApi logout call.")
        return True
    