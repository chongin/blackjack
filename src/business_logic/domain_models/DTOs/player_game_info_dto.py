from data_models.player_game_info import PlayerGameInfo, PlayerGameInfos, BankerGameInfo
from data_models.card import Cards
from business_logic.domain_models.DTOs.card_dto import CardsDto
from business_logic.domain_models.DTOs.bet_option_dto import BetOptionsDTO


class PlayerGameInfoDTO:
    @classmethod
    def from_data_model(cls, player_game_info: PlayerGameInfo) -> 'PlayerGameInfosDTO':
        return cls(player_game_info) 

    def __init__(self, player_game_info: PlayerGameInfo) -> None:
        self.player_id = player_game_info.player_id
        self.first_two_cards = CardsDto.from_data_model(player_game_info.first_two_cards)
        self.hit_cards = CardsDto.from_data_model(player_game_info.hit_cards)
        self.is_stand = player_game_info.is_stand
        self.bet_options = BetOptionsDTO.from_data_model(player_game_info.bet_options)
        self.result = player_game_info.result

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "first_two_cards": self.first_two_cards.to_list(),
            "hit_cards": self.hit_cards.to_list(),
            "is_stand": self.is_stand,
            "bet_options": self.bet_options.to_list(),
            "result": self.result
        }


class BankerGameInfoDTO:
    @classmethod
    def from_data_model(cls, banker_game_info: BankerGameInfo) -> 'BankerGameInfoDTO':
        return cls(banker_game_info) 

    def __init__(self, banker_game_info: PlayerGameInfo) -> None:
        self.first_two_cards = CardsDto.from_data_model(banker_game_info.first_two_cards)
        self.hit_cards = CardsDto.from_data_model(banker_game_info.hit_cards)
        self.is_stand = banker_game_info.is_stand
        self.result = banker_game_info.result

    def to_dict(self) -> dict:
        return {
            "first_two_cards": self.first_two_cards.to_list(),
            "hit_cards": self.hit_cards.to_list(),
            "is_stand": self.is_stand,
            "result": self.result
        }

class PlayerGameInfosDTO(list):
    @classmethod
    def from_data_model(cls, player_game_infos: PlayerGameInfos) -> 'PlayerGameInfosDTO':
        return cls(player_game_infos)

    def __init__(self, player_game_infos: PlayerGameInfos) -> None:
        for data in player_game_infos:
            self.append(PlayerGameInfoDTO(data))

    def to_list(self) -> list[dict]:
        return [item.to_dict() for item in self]
