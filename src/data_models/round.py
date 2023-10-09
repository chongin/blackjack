from data_models.deal_cards import PlayerCards, BankerCards
from data_models.result import Result


class RoundState:
    def __init__(self, state) -> None:
        pass


class Round:
    def __init__(self, data: dict) -> None:
        self.round_id = data['round_id']
        self.deck_id = data['deck_id']
        self.hand = data['hand']
        self.state = data['state']
        self.player_cards = PlayerCards(data['player_cards'])
        self.banker_cards = BankerCards(data['banker_cards'])
        self.has_black_card = data['has_black_card']
        self.result = Result(data['result'])
        self.started_at = data['started_at']
        self.ended_at = data['ended_at']
        self.created_at = data['created_at']
        self.ended_at = data['ended_at']
