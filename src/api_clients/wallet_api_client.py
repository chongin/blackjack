from api_clients.api_client_base import ApiClientBase


class WalletApi(ApiClientBase):
    def __init__(self, endpoint='https://www.mock_wallet.com', timeout=10) -> None:
        super().__init__(endpoint, timeout)

    def deposit(self, wallet_info: dict) -> bool:
        return True

    def withdraw(self, wallet_info: dict) -> bool:
        return True
