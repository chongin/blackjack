from data_models.result import PlayerResult, Result
from data_models.bet_option import BetOptions
from business_logic.domain_models.bet_option_dto import BetOptionsDTO


class PlayerResultDTO:
    @classmethod
    def from_data_model(cls, player_result: PlayerResult) -> 'PlayerResultDTO':
        return cls(
            player_id=player_result.player_id,
            bet_options=player_result.bet_options,
            player_total_point=player_result.player_total_point,
            banker_total_point=player_result.banker_total_point
        )

    def __init__(self, player_id: str, bet_options: BetOptions,
                 player_total_point: int, banker_total_point: int) -> None:
        self.player_id = player_id
        self.bet_options = BetOptionsDTO.from_data_model(bet_options)
        self.player_total_point = player_total_point
        self.banker_total_point = banker_total_point

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "bet_options": self.bet_options.to_list(),
            "player_total_point": self.player_total_point,
            "banker_total_point": self.banker_total_point
        }


class ResultDTO(list):
    @classmethod
    def from_data_model(cls, result: Result) -> 'ResultDTO':
        return cls(
            datalist=result,
        )

    def __init__(self, datalist: list[PlayerResult]) -> None:
        for data in datalist:
            self.append(PlayerResultDTO.from_data_model(data))

    def to_list(self) -> list[dict]:
        return [item.to_dict() for item in self]