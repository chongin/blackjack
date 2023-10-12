from data_models.round import Round
from data_models.player_game_info import PlayerGameInfo

class RoundRepository:
    def __init__(self, round: Round) -> None:
        self.round = Round

    def find_player_game_info_by_player_id(self, player_id: str) -> PlayerGameInfo:
        for player_game_info in self.round.player_game_infos:
            if player_game_info.player_id == player_id:
                return player_game_info
        return None
    
    def retrieve_first_player_game_info(self) -> PlayerGameInfo:
        if len(self.round.player_game_infos) > 0:
            return self.round.player_game_infos[0]
        return None

    def retrieve_next_player_game_info(self, prev_player_id: str) -> PlayerGameInfo:
        for player_game_info in self.round.player_game_infos:
            pass
    