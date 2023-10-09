from data_models.bet_option import BetOptions


class PlayerResult:
    def __init__(self, data: dict) -> None:
        self.player_id = data['player_id']
        self.total_point = data['total_point']
        self.banker_total_point = data['total_win']
        self.bet_options = BetOptions(data['bet_options'])


class Result(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(PlayerResult(data))
