from data_models.card import Cards


class DealCard:
    def __init__(self, data: dict) -> None:
        self.first_two_cards = Cards(data['first_two_cards'])
        self.hit_cards = Cards(data['hit_cards'])

    def to_dict(self) -> dict:
        deal_card_dict = {
            'first_two_cards': self.first_two_cards.to_list(),
            'hit_cards': self.hit_cards.to_list(),
        }
        return deal_card_dict


class DealCards(list):
    def __init__(self, deal_cards: list):
        for deal_card_data in deal_cards:
            self.append(DealCard(deal_card_data))
    
    def to_list(self) -> list:
        return [item.to_dict() for item in self]


class PlayerCards(DealCards):
    pass


class BankerCards(DealCards):
    pass
