from data_models.round import Round
from data_models.round_histories import RoundHistories
from data_models.card import Cards

class Deck:
    def __init__(self, data: dict) -> None:
        self.deck_id = data['deck_id']
        self.shoe_id = data['shoe_id']
        self.deck_api_id = data['deck_api_id']
        self.deal_cards = Cards(data['deal_cards'])
        self.remaind_count_of_cards = data['remaind_count_of_cards']
        self.black_card_postion = data['black_card_postion']
        self.state = data['state']
        self.started_at = data['started_at']
        self.ended_at = data['ended_at']

        self.current_round = Round(data['current_round'])
        self.round_histories = RoundHistories(data['round_histories'])
