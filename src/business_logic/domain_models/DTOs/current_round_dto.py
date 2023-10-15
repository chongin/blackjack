from data_models.round import Round
from data_models.player_game_info import PlayerGameInfos, BankerGameInfo
from business_logic.domain_models.DTOs.player_game_info_dto import PlayerGameInfosDTO, BankerGameInfoDTO

class CurrentRoundDTO:
    @classmethod
    def from_data_model(cls, round: Round) -> 'CurrentRoundDTO':
        return cls(round)

    def __init__(self, round: Round) -> None:
        self.round_id = round.round_id
        self.state = round.state
        self.hand = round.hand
        self.player_game_infos = PlayerGameInfosDTO.from_data_model(round.player_game_infos)
        self.banker_game_info = BankerGameInfoDTO.from_data_model(round.banker_game_info)
            

        # only have one banker, so change it to dict
        if len(self.banker_game_info) > 0:
            self.banker_game_info = self.banker_game_info[0]
        else:
            self.banker_game_info = {}

        self.has_black_card = round.has_black_card

    def to_dict(self) -> dict:
        hash = {
            "round_id": self.round_id,
            "state": self.state,
            "hand": self.hand,
            "has_black_card": self.has_black_card
        }

        # it should be call filter_by_player_id first.
        if type(self.player_game_infos) is dict:
            hash["player_game_infos"] = {}
        else:
            hash["player_game_infos"] = self.player_game_infos.to_dict()
        
        # it should be call filter_by_player_id first.
        if type(self.banker_game_info) is dict:
            hash["banker_game_info"] = {}
        else:
            hash["banker_game_info"] = self.banker_game_info.to_dict()

        return hash

    def filter_by_player_id(self, player_id: str) -> None:
        for player_game_info in self.player_game_infos:
            if player_game_info.player_id == player_id:
                self.player_game_infos = player_game_info
                return
        self.player_game_infos = {}