from data_models.bet_option import BetOption, BetOptions


class BetOptionDTO:
    def from_data_model(cls, bet_option: BetOption) -> 'BetOptionDTO':
        return cls(
            option_name=bet_option.option_name,
            bet_amt=bet_option.bet_amt,
            win_amt=bet_option.win_amt
        )

    def __init__(self, option_name: str, bet_amt: int, win_amt: int) -> None:
        self.option_name = option_name
        self.bet_amt = bet_amt
        self.win_amt = win_amt

    def to_dict(self) -> dict:
        return {
            "option_name": self.option_name,
            "bet_amt": self.bet_amt,
            "win_amt": self.win_amt
        }
    

class BetOptionsDTO(list):
    @classmethod
    def from_data_model(cls, bet_options: BetOptions) -> 'BetOptionsDTO':
        return cls(
            datalist=bet_options,
        )

    def __init__(self, datalist: list[BetOption]) -> None:
        for data in datalist:
            self.append(BetOptionDTO.from_data_model(data))

    def to_list(self) -> list[dict]:
        return [item.to_dict() for item in self]
