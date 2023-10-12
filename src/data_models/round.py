from data_models.player_game_info import PlayerGameInfos, BankerGameInfo, PlayerGameInfo
from ulid import ULID
from utils.util import Util


class RoundState:
    OPENED = "opened"
    BET_STARTED = "bet_started"
    BET_ENDED = "bet_ended"
    DEAL_STARTED = "deal_started"
    DEAL_ENDED = "deal_ended"
    RESULTED = "resulted"
    CLOSED = "closed"


class Round:
    @classmethod
    def new_model(cls, deck_index: int) -> 'Round':
        round_data = {
            'round_id': str(ULID()),
            'deck_index': deck_index,
            'hand': 0,
            'state': RoundState.OPENED,
            'player_game_infos': [],
            'banker_game_info': [],
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
        self.player_game_infos = PlayerGameInfos(data['player_game_infos']) if data.get('player_game_infos') else PlayerGameInfos([])
        self.banker_game_info = BankerGameInfo(data['banker_game_info']) if data.get('banker_game_info') else {}
        self.has_black_card = data['has_black_card']
        self.started_at = data.get('started_at')
        self.ended_at = data.get('ended_at')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # when init data, should set parent object here
    def set_parent(self, deck: any) -> None:
        self.deck = deck

    def to_dict(self) -> dict:
        round_hash = {
            'round_id': self.round_id,
            'deck_index': self.deck_index,
            'hand': self.hand,
            'state': self.state,
            'player_game_infos': self.player_game_infos.to_list(),
            'has_black_card': self.has_black_card,
            'started_at': self.started_at,
            'ended_at': self.ended_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

        if type(self.banker_game_info) is dict:
            round_hash['banker_game_info'] = {}
        else:
            round_hash['banker_game_info'] = self.banker_game_info.to_dict()
        return round_hash
    

    def notify_info(self) -> dict:
        info = {
            'round_id': self.round_id,
            'deck_index': self.deck_index,
            'hand': self.hand,
            'state': self.state,
            'shoe_name': self.deck.shoe.shoe_name,
            'started_at': self.started_at,
            'ended_at': self.ended_at,
        }

        info.update(self.deck.shoe.notify_info())
        return info
    
    def can_bet(self) -> bool:
        return self.state == RoundState.OPENED or self.state == RoundState.BET_STARTED

    def can_interaction(self) -> bool:
        return self.state == RoundState.DEAL_ENDED or self.state == RoundState.OPENED # need change
    
    def is_opened(self) -> bool:
        return self.state == RoundState.OPENED
    
    def is_bet_started(self) -> bool:
        return self.state == RoundState.BET_STARTED
    
    def is_bet_ended(self) -> bool:
        return self.state == RoundState.BET_ENDED
    
    def is_deal_started(self) -> bool:
        return self.state == RoundState.DEAL_STARTED
    
    def is_deal_ended(self) -> bool:
        return self.state == RoundState.DEAL_ENDED
    
    def is_resultedd(self) -> bool:
        return self.state == RoundState.RESULTED
    
    def is_closed(self) -> bool:
        return self.state == RoundState.CLOSED
    
    def set_bet_started(self):
        self.state = RoundState.BET_STARTED
    
    def set_bet_ended(self):
        self.state = RoundState.BET_ENDED

    def set_deal_started(self):
        self.state = RoundState.DEAL_STARTED

    def set_deal_ended(self):
        self.state = RoundState.DEAL_ENDED

    def set_resulted(self):
        self.state = RoundState.RESULTED

    def set_closed(self):
        self.state = RoundState.CLOSED