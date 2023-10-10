from data_models.card import Cards


class DealCard:
    def __init__(self, data: dict) -> None:
        self.player_id = data['player_id']
        self.first_two_cards = Cards(data['first_two_cards'])
        self.hit_cards = Cards(data['hit_cards'])
        self.is_stand = data['is_stand'] if data.get('is_stand') else False

    def to_dict(self) -> dict:
        deal_card_dict = {
            'player_id': self.player_id,
            'first_two_cards': self.first_two_cards.to_list(),
            'hit_cards': self.hit_cards.to_list(),
            'is_stand': self.is_stand
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

#Banker only have one
class BankerCards(DealCards):
    pass
