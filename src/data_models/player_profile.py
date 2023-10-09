from data_models.base_model import BaseModel


class Wallet:
    def __init__(self, data: dict) -> None:
        self.balance = data['balance']
        self.total_win = data['total_win']
        self.total_lost = data['total_lost']


class PlayerProfile(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.player_id = data['player_id']
        self.state = data['state']
        self.state = data['state']
        self.wallet = Wallet(data['wallet'])
        