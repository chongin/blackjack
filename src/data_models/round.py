from data_models.deal_cards import PlayerCards, BankerCards
from data_models.result import Result, PlayerResult
from ulid import ULID
from utils.util import Util


class RoundState:
    def __init__(self, state) -> None:
        self.states = {
            "opened": 1,
            "bet_started": 2,
            "bet_ended": 3,
            "deal_started": 4,
            "deal_ended": 5,
            "resulted": 6,
            "closed": 7
        }


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
        self.player_cards = PlayerCards(data['player_cards']) if data.get('player_cards') else PlayerCards([])
        self.banker_cards = BankerCards(data['banker_cards']) if data.get('banker_cards') else BankerCards([])
        self.has_black_card = data['has_black_card']
        self.result = Result(data['result']) if data.get('result') else Result([])
        self.started_at = data.get('started_at')
        self.ended_at = data.get('ended_at')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def to_dict(self) -> dict:
        round_hash = {
            'round_id': self.round_id,
            'deck_index': self.deck_index,
            'hand': self.hand,
            'state': self.state,
            'player_cards': self.player_cards.to_list(),
            'banker_cards': self.banker_cards.to_list(),
            'has_black_card': self.has_black_card,
            'result': self.result.to_list(),
            'started_at': self.started_at,
            'ended_at': self.ended_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

        return round_hash
    
    def can_bet(self) -> bool:
        return self.state == 'opened' or self.state == 'bet_started'

    def can_interaction(self) -> bool:
        return self.state == 'deal_ended'
    
    def find_player_result_by_id(self, player_id: str) -> PlayerResult:
        return self.result.get_player_result_by_id(player_id)
