from data_models.round import Round


class RoundHistories(list):
    def __init__(self, datalist) -> None:
        for data in datalist:
            self.append(Round(data))

    def to_list(self) -> list:
        round_list = []
        for round in self:
            round_list.append(round.to_dict())
        return round_list
