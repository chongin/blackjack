from configuration.system_config import SystemConfig
from exceptions.system_exception import ParameterWrongException

class BetOptionReq:
    def __init__(self, data: dict) -> None:
        self.option_name = data['option_name']
        self.bet_amt = data['bet_amt']

    def to_dict(self) -> dict:
        bet_option_data = {
            'option_name': self.option_name,
            'bet_amt': self.bet_amt,
        }
        return bet_option_data

    def validate(self) -> bool:
        if self.option_name not in SystemConfig.instance().bet_option_names:
            raise ParameterWrongException(f"This option name: {self.option_name} is not suppported.")
        
        if type(self.bet_amt) is not int:
            raise ParameterWrongException(f"Bet amt is wrong type, please use integer.")
        
        if (int)(self.bet_amt) <= 0:
            raise ParameterWrongException(f"Bet amt value is not valid, it should be greater than zero.")
        return True


class BetOptionsReq(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(BetOptionReq(data))

    def to_list(self) -> list:
        return [item.to_dict() for item in self]

    def validate(self) -> bool:
        for item in self:
            item.validate()
        return True

    def get_total_bet_amt(self) -> int:
        sum = 0
        for item in self:
            sum += (int)(item.bet_amt)
        return sum