from data_models.card import Card, Cards


class CardDTO:
    @classmethod
    def from_data_model(cls, card: Card) -> 'CardDTO':
        return cls(
            card_code=card.player_id,
            suit=card.player_name,
            value=card.value
        )

    def __init__(self, card_code: str, suit: str, value: str) -> None:
        self.card_code = card_code
        self.suit = suit
        self.value = value
        self.image_url = self._compose_image_url()

    def _compose_image_url(self) -> str:
        return f"https://deckofcardsapi.com/static/img/{self.car_code}.png"

    def to_dict(self) -> dict:
        return {
            "card_code": self.card_code,
            "suit": self.suit,
            "value": self.value,
            "image_url": self.image_url
        }


class CardsDto(list):
    @classmethod
    def from_data_model(cls, cards: Cards) -> 'CardsDto':
        return cls(
            datalist=cards,
        )

    def __init__(self, datalist: list[Card]) -> None:
        for data in datalist:
            self.append(CardDTO.from_data_model(data))

    def to_list(self) -> list[dict]:
        return [item.to_dict() for item in self]