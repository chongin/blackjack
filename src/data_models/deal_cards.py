from data_models.card import Cards


class DealCard:
    def __init__(self, data: dict) -> None:
        self.first_two_cards = Cards(data['first_two_cards'])
        self.hit_cards = Cards(data['hit_cards'])


class DealCards(list):
    def __init__(self, deal_cards: list):
        for deal_card in deal_cards:
            pass


class PlayerCards(DealCards):
    pass


class BankerCards(DealCards):
    pass
