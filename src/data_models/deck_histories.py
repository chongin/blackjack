from data_models.deck import Deck


class DeckHistories(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(Deck(data))

    def to_list(self) -> list:
        deck_list = []
        for deck in self:
            deck_list.append(deck.to_dict())
        return deck_list