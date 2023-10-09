from data_models.deal_cards import PlayerCards, BankerCards
from data_models.result import Result
from ulid import ULID
from utils.util import Util


class RoundState:
    def __init__(self, state) -> None:
        pass


class Round:
    @classmethod
    def new_model(cls, deck_index: int) -> 'Round':
        round_data = {
            'round_id': str(ULID()),
            'deck_index': deck_index,
            'hand': 0,
            'state': 'opened',
            'player_cards': [],
            'banker_cards': [],
            'has_black_card': False,
            'result': [],
            'started_at': None,
            'ended_at': None,
            'created_at': Util.current_utc_time(),
            'updated_at': Util.current_utc_time()
        }

        return cls(round_data)
    
    def __init__(self, data: dict) -> None:
        self.round_id = data['round_id']
        self.deck_index = data['deck_index']
        self.hand = data['hand']
        self.state = data['state']
        self.player_cards = PlayerCards(data['player_cards'])
        self.banker_cards = BankerCards(data['banker_cards'])
        self.has_black_card = data['has_black_card']
        self.result = Result(data['result'])
        self.started_at = data['started_at']
        self.ended_at = data['ended_at']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
