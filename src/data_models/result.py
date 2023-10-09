from data_models.bet_option import BetOptions


class PlayerResult:
    def __init__(self, data: dict) -> None:
        self.player_id = data['player_id']
        self.total_point = data['total_point']
        self.banker_total_point = data['total_win']
        self.bet_options = BetOptions(data['bet_options'])

    def to_dict(self) -> dict:
        result_data = {
            'player_id': self.player_id,
            'total_point': self.total_point,
            'banker_total_point': self.banker_total_point,
            'bet_options': self.bet_options.to_dict(),
        }
        return result_data


class Result(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(PlayerResult(data))

    def to_list(self) -> list:
        result_list = []
        for player_result in self:
            result_list.append(player_result.to_dict())
        return result_list
