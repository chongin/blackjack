from data_models.round import Round
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
        self.deck_index = data['deck_index']
        self.shoe_id = data['shoe_id']
        self.deck_api_id = data['deck_api_id']
        self.deal_cards = Cards(data['deal_cards']) if data.get('deal_cards') else Cards([])
        self.remaind_count_of_cards = data['remaind_count_of_cards']
        self.black_card_postion = data['black_card_postion']
        self.state = data['state']
        self.started_at = data['started_at']
        self.ended_at = data.get('ended_at')

        self.current_round = Round(data['current_round']) if data.get('current_round') else None #should check it
        # self.round_histories = RoundHistories(data['round_histories']) if data.get('round_histories') else RoundHistories([])
        if self.current_round is not None:
            self.current_round.set_parent(self)

    # when init data, should set parent object here
    def set_parent(self, shoe: any) -> None:
        self.shoe = shoe

    def to_dict(self) -> dict:
        deck_hash = {
            'deck_index': self.deck_index,
            'shoe_id': self.shoe_id,
            'deck_api_id': self.deck_api_id,
            'deal_cards': self.deal_cards.to_list(),
            'remaind_count_of_cards': self.remaind_count_of_cards,
            'black_card_postion': self.black_card_postion,
            'state': self.state,
            'started_at': self.started_at,
            'ended_at': self.ended_at,
        }

        if self.current_round:
            deck_hash['current_round'] = self.current_round.to_dict()

        return deck_hash