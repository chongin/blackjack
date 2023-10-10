from data_models.player_profile import PlayerProfile


class PlayerProfileDTO:
    @classmethod
    def from_data_model(cls, player_profile: PlayerProfile) -> 'PlayerProfileDTO':
        return cls(
            player_id=player_profile.player_id,
            player_name=player_profile.player_name,
            balance=player_profile.wallet.balance
        ) 

    def __init__(self, player_id: str, player_name: str, balance: int) -> None:
        self.player_id = player_id
        self.player_name = player_name
        self.balance = balance

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "balance": self.balance
        }