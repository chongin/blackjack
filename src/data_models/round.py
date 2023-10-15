from data_models.player_game_info import PlayerGameInfos, BankerGameInfo, PlayerGameInfo
from ulid import ULID
from utils.util import Util
from exceptions.system_exception import StateMachineException

class RoundState:
    OPENED = "opened"
    BET_STARTED = "bet_started"
    BET_ENDED = "bet_ended"
    DEAL_STARTED = "deal_started"
    DEAL_ENDED = "deal_ended"
    PLAYERS_STANDED = 'players_standed'
    BANKER_STANDED = 'banker_standed'
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
            'bet_started_at': None,
            'bet_ended_at': None,
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
        self.banker_game_info = BankerGameInfo(data['banker_game_info']) if data.get('banker_game_info') else BankerGameInfo.generate_default_ins()
        self.has_black_card = data['has_black_card']
        self.bet_started_at = data.get('bet_started_at')
        self.bet_ended_at = data.get('bet_ended_at')
        self.deal_card_sequences = data.get('deal_card_sequences') if data.get('deal_card_sequences') else []
        self.hit_card_sequences = data.get('hit_card_sequences') if data.get('hit_card_sequences') else []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # when init data, should set parent object here
    def set_parent(self, deck: any) -> None:
        self.deck = deck

    def to_dict(self) -> dict:
        hash = {
            'round_id': self.round_id,
            'deck_index': self.deck_index,
            'hand': self.hand,
            'state': self.state,
            'player_game_infos': self.player_game_infos.to_list(),
            'banker_game_info': self.banker_game_info.to_dict(),
            'has_black_card': self.has_black_card,
            'bet_started_at': self.bet_started_at,
            'bet_ended_at': self.bet_ended_at,
            'deal_card_sequences': self.deal_card_sequences,
            'hit_card_sequences': self.hit_card_sequences,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        return hash   

    def notify_info(self) -> dict:
        info = {
            'round_id': self.round_id,
            'deck_index': self.deck_index,
            'hand': self.hand,
            'state': self.state,
            'shoe_name': self.deck.shoe.shoe_name,
            'bet_started_at': self.bet_started_at,
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
    
    def is_players_standed(self) -> bool:
        return self.state == RoundState.PLAYERS_STANDED
    
    def is_banker_standed(self) -> bool:
        return self.state == RoundState.BANKER_STANDED
    
    def is_resultedd(self) -> bool:
        return self.state == RoundState.RESULTED
    
    def is_closed(self) -> bool:
        return self.state == RoundState.CLOSED
    
    def set_bet_started(self):
        if self.is_opened():
            self.state = RoundState.BET_STARTED
        else:
            raise StateMachineException(f"Can not change to bet_started from this state: {self.state}")
    
    def set_bet_ended(self):
        if self.is_bet_started():
            self.state = RoundState.BET_ENDED
        else:
            raise StateMachineException(f"Can not change to bet_ended from this state: {self.state}")
        
    def set_deal_started(self):
        if self.is_bet_ended() or self.is_deal_started():
            self.state = RoundState.DEAL_STARTED
        else:
            raise StateMachineException(f"Can not change to deal_started from this state: {self.state}")

    def set_deal_ended(self):
        self.state = RoundState.DEAL_ENDED

    def set_players_standed(self):
        self.state = RoundState.PLAYERS_STANDED

    def set_banker_standed(self):
        self.state = RoundState.BANKER_STANDED

    def set_resulted(self):
        self.state = RoundState.RESULTED

    def set_closed(self):
        self.state = RoundState.CLOSED

    def find_player_game_info_by_player_id(self, player_id: str) -> PlayerGameInfo:
        for player_game_info in self.player_game_infos:
            if player_game_info.player_id == player_id:
                return player_game_info
        return None

    def get_all_player_id_have_betted(self) -> list[str]:
        all_bet_player_ids = []
        for player_game_info in self.player_game_infos:
            if player_game_info.bet_options:
                all_bet_player_ids.append(player_game_info.player_id)

        return all_bet_player_ids