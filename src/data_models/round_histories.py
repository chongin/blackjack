from data_models.round import Round


class RoundHistories(list):
    def __init__(self, datalist) -> None:
        for data in datalist:
            self.append(Round(data))

    def to_list(self) -> list:
        return [item.to_dict() for item in self]
