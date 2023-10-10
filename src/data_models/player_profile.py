from data_models.base_model import BaseModel
from data_models.db_conn.firebase_client import FirebaseClient
from ulid import ULID

class Wallet:
    def __init__(self, data: dict) -> None:
        self.balance = data['balance']
        self.total_win = data['total_win']
        self.total_lost = data['total_lost']

    def to_dict(self) -> dict:
        wallet_dict = {
            'balance': self.balance,
            'total_win': self.total_win,
            'total_lost': self.total_lost,
        }
        return wallet_dict


class PlayerProfile:
    @classmethod
    def new_model(cls, player_name: str) -> 'PlayerProfile':
        player_profile_hash = {
            'player_id': str(ULID()),
            'player_name': player_name,
            'state': 'active',
            'wallet': {
                'balance': 500,
                'total_win': 0,
                'total_lost': 0
            }
        }

        return cls(player_profile_hash)

    def __init__(self, data: dict) -> None:
        self.player_id = data['player_id']
        self.player_name = data['player_name']
        self.state = data['state']
        self.wallet = Wallet(data['wallet'])

    def to_dict(self) -> dict:
        player_profile_dict = {
            'player_id': self.player_id,
            'player_name': self.player_name,
            'state': self.state,
            'wallet': self.wallet.to_dict(),
        }
        return player_profile_dict


class PlayerProfiles(list):
    def __init__(self, datalist: list):
        for data in datalist:
            self.append(PlayerProfile(data))

    def to_list(self) -> list:
        player_profile_list = []
        for player_profile in self:
            player_profile_list.append(player_profile.to_dict())
        return player_profile_list