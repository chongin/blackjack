class BetOption:
    def __init__(self, data: dict) -> None:
        self.option_name = data['option_name']
        self.bet_amt = data['bet_amt']
        self.win_amt = data.get('win_amt')
        self.result = data.get('result')  # win draw lost

    def to_dict(self) -> dict:
        bet_option_data = {
            'option_name': self.option_name,
            'bet_amt': self.bet_amt,
            'win_amt': self.win_amt,
            'result': self.result
        }
        return bet_option_data

class BetOptions(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(BetOption(data))

    def to_list(self) -> list:
        return [item.to_dict() for item in self]
