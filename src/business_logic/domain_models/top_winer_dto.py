from data_models.player_profile import PlayerProfile


class TopWinerDTO:
    @classmethod
    def from_data_model(cls, player_profile: PlayerProfile) -> 'PlayerProfileDTO':
        return cls(
            player_id=player_profile.player_id,
            player_name=player_profile.player_name,
            total_win=player_profile.wallet.total_win
        ) 

    def __init__(self, player_id: str, player_name: str, total_win: int) -> None:
        self.player_id = player_id
        self.player_name = player_name
        self.total_win = total_win

    def to_dict(self) -> dict:
        {
            'player_id': self.player_id,
            'player_name': self.player_name,
            'total_win': self.total_win
        }


class TopWinnersDTO(list):
    @classmethod
    def from_data_model(cls, top_winners: list[PlayerProfile]) -> 'ResultDTO':
        return cls(
            datalist=top_winners,
        )

    def __init__(self, datalist: list[PlayerProfile]) -> None:
        for data in datalist:
            self.append(TopWinerDTO.from_data_model(data))

    def to_list(self) -> list[dict]:
        return [item.to_dict() for item in self]
