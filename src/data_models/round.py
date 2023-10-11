from data_models.player_game_infos import PlayerGameInfos, BankerGameInfo, PlayerGameInfo
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
    
    def can_bet(self) -> bool:
        return self.state == 'opened' or self.state == 'bet_started'

    def can_interaction(self) -> bool:
        return self.state == 'deal_ended' or self.state == 'opened' # need change
    
    def find_player_game_info_by_player_id(self, player_id: str) -> PlayerGameInfo:
        for player_game_info in self.player_game_infos:
            if player_game_info.player_id == player_id:
                return player_game_info
        return None
