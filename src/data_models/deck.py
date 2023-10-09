from data_models.round import Round
from data_models.round_histories import RoundHistories
from data_models.card import Cards
from utils.util import Util
import random


class Deck:
    @classmethod
    def new_model(cls, shoe_id: str, deck_index: int, deck_api_id: str,
                  remaind_count_of_cards: int) -> 'Deck':
        black_card_postion = cls.generate_blackcard_random_number(
            remaind_count_of_cards
        )
        deck_data = {
            'deck_index': deck_index,
            'shoe_id': shoe_id,
            'deck_api_id': deck_api_id,
            'deal_cards': [],
            'remaind_count_of_cards': remaind_count_of_cards,
            'black_card_postion': black_card_postion,
            'state': 'active',
            'started_at': Util.current_utc_time(),
            'ended_at': None,
            'current_round': None,
            'round_histories': []
        }

        return cls(deck_data)
    
    @classmethod
    def generate_blackcard_random_number(cls, number: int):
        lower_bound = 3/4 * number
        upper_bound = lower_bound + 1/8 * number

        random_number = (int)(random.uniform(lower_bound, upper_bound))
        return random_number
    
    def __init__(self, data: dict) -> None:
        print(f"deck........ {data}")
        self.deck_index = data['deck_index']
        self.shoe_id = data['shoe_id']
        self.deck_api_id = data['deck_api_id']
        self.deal_cards = Cards(data['deal_cards'])
        self.remaind_count_of_cards = data['remaind_count_of_cards']
        self.black_card_postion = data['black_card_postion']
        self.state = data['state']
        self.started_at = data['started_at']
        self.ended_at = data['ended_at']

        self.current_round = Round(data['current_round']) if data.get('current_round') else None
        self.round_histories = RoundHistories(data['round_histories'])
