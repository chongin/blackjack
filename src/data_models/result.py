from data_models.bet_option import BetOptions


class PlayerResult:
    def __init__(self, data: dict) -> None:
        self.player_id = data['player_id']
        self.player_total_point = data.get('player_total_point')
        self.banker_total_point = data.get('total_win')
        self.bet_options = BetOptions(data['bet_options'])

    def to_dict(self) -> dict:
        result_data = {
            'player_id': self.player_id,
            'player_total_point': self.player_total_point,
            'banker_total_point': self.banker_total_point,
            'bet_options': self.bet_options.to_list(),
        }
        return result_data

    def add_player_bet_options(self,  bet_options: BetOptions) -> None:
        for bet_option in bet_options:
            self.bet_options.append(bet_option)


class Result(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(PlayerResult(data))

    def to_list(self) -> list:
        return [item.to_dict() for item in self]

    def get_player_result_by_id(self, player_id: str) -> PlayerResult:
        for player_result in self:
            if player_result.player_id == player_id:
                return player_result
        return None

