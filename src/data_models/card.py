class Card:
    CARD_POINTS = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'JACK': 10,
        'QUEEN': 10,
        'KING': 10,
        'ACE': 1
    }

    def __init__(self, data: dict) -> None:
        self.code = data['code']
        self.value = data['value']
        self.suit = data['suit']
        self.received_at = data['received_at']

    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'value': self.value,
            'suit': self.suit,
            'received_at': self.received_at,
        }

    def point(self) -> int:
        return self.CARD_POINTS[self.value]

    def ace_point(self) -> int:
        if self.value == 'ACE':
            return 11
        return self.point()


class Cards(list):
    def __init__(self, datalist: list) -> None:
        for data in datalist:
            self.append(Card(data))

    def to_list(self) -> list:
        return [item.to_dict() for item in self]


class BalckCard(Card):
    pass
