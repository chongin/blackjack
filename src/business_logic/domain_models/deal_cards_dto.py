from data_models.deal_cards import DealCard, DealCards
from data_models.card import Cards
from business_logic.domain_models.card_dto import CardsDto


class DealCardDto:
    @classmethod
    def from_data_model(cls, deal_card: DealCard) -> 'DealCardsDto':
        return cls(
            first_two_cards=deal_card.first_two_cards,
            hit_cards=deal_card.hit_cards,
        ) 

    def __init__(self, first_two_cards: DealCard, hit_cards: DealCard) -> None:
        self.first_two_cards = CardsDto.from_data_model(first_two_cards)
        self.hit_cards = CardsDto.from_data_model(hit_cards)


class DealCardsDto(list):
    @classmethod
    def from_data_model(cls, deal_cards: DealCards) -> 'DealCardsDto':
        return cls(
            datalist=deal_cards
        ) 

    def __init__(self, datalist: list[DealCard]) -> None:
        for data in datalist:
            self.append(DealCardDto(data))

    def to_list(self) -> list[dict]:
        return [item.to_dict() for item in self]
