class BetOption:
    def __init__(self, data: dict) -> None:
        self.option_name = data['option_name']
        self.bet_amt = data['bet_amt']
        self.win_amt = data['win_amt']


class BetOptions(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(BetOption(data))