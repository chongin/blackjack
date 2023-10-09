from data_models.base_model import BaseModel


class Card:
    def __init__(self, data: dict) -> None:
        self.round_id = data['round_id']
        self.hand = data['hand']
        self.card_code = data['card_code']
        self.value = data['value']
        self.suit = data['suit']
        self.received_at = data['received_at']
        self.image_url = self._compose_image_url()

    def _compose_image_url(self) -> str:
        return ""

    def to_dict(self) -> dict:
        return {
            'round_id': self.round_id,
            'hand': self.hand,
            'card_code': self.card_code,
            'value': self.value,
            'suit': self.suit,
            'received_at': self.received_at,
            'image_url': self.image_url,
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
