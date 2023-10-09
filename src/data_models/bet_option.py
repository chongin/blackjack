class BetOption:
    def __init__(self, data: dict) -> None:
        self.option_name = data['option_name']
        self.bet_amt = data['bet_amt']
        self.win_amt = data['win_amt']

    def to_dict(self) -> dict:
        bet_option_data = {
            'option_name': self.option_name,
            'bet_amt': self.bet_amt,
            'win_amt': self.win_amt,
        }
        return bet_option_data


class BetOptions(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(BetOption(data))

    def to_list(self) -> list:
        bet_options_list = []
        for bet_option in self:
            bet_options_list.append(bet_option.to_dict())
        return bet_options_list