from data_models.deck import Deck


class DeckHistories(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(Deck(data))
