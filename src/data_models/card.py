from data_models.base_model import BaseModel


class Card:
    def __init__(self, data: dict) -> None:
        self.card_code = data['card_code']
        self.value = data['value']
        self.suit = data['suit']
        self.received_at = data['received_at']
        

    def to_dict(self) -> dict:
        return {
            'card_code': self.card_code,
            'value': self.value,
            'suit': self.suit,
            'received_at': self.received_at,
        }


class Cards(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(Card(data))

    def to_list(self) -> list:
        card_list = []
        for card in self:
            card_list.append(card.to_dict())
        return card_list
    

class BalckCard(Card):
    pass
