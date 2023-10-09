from data_models.card import Card
from data_models.deal_cards import PlayerCards, BankerCards


class Round:
    def __init__(self, data: dict) -> None:
        self.round_id = data['round_id']
        self.deck_id = data['deck_id']
        self.hand = data['hand']
        self.state = data['state']
        self.player_cards = PlayerCards(data['player_cards'])
        self.banker_cards = BankerCards(data['banker_cards'])
        self.has_black_card = data['has_black_card']
        self.result = ''
        self.started_at = data['started_at']
        self.ended_at = data['ended_at']
        self.created_at = data['created_at']
        self.ended_at = data['ended_at']
