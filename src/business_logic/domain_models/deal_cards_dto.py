from data_models.deal_cards import DealCard, DealCards
from data_models.card import Cards
from business_logic.domain_models.card_dto import CardsDto


class DealCardDto:
    @classmethod
    def from_data_model(cls, deal_card: DealCard) -> 'DealCardsDto':
        return cls(
            player_id=deal_card.player_id,
            first_two_cards=deal_card.first_two_cards,
            hit_cards=deal_card.hit_cards,
            is_stand=deal_card.is_stand
        ) 

    def __init__(self, player_id: str, first_two_cards: DealCard,
                 hit_cards: DealCard, is_stand: bool) -> None:
        self.player_id = player_id
        self.first_two_cards = CardsDto.from_data_model(first_two_cards)
        self.hit_cards = CardsDto.from_data_model(hit_cards)
        self.is_stand = is_stand


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
