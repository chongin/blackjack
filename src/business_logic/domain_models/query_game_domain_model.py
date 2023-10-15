from data_models.shoe import Shoe
from data_models.player_profile import PlayerProfile
from business_logic.domain_models.DTOs.player_profile_dto import PlayerProfileDTO
from business_logic.domain_models.DTOs.top_winer_dto import TopWinnersDTO
from business_logic.domain_models.DTOs.current_round_dto import CurrentRoundDTO

class QueryGameDomainModel:
    def __init__(self, shoe: Shoe, player_profile: PlayerProfile, top_winners: list[PlayerProfile]) -> None:
        self.table_name = shoe.shoe_name
        self.config = shoe.config.to_dict()
        self.player_profile_dto = PlayerProfileDTO.from_data_model(player_profile)
        self.current_round_dto = CurrentRoundDTO.from_data_model(shoe.current_deck.current_round)
        self.top_winners_dto = TopWinnersDTO.from_data_model(top_winners)

    def to_dict(self) -> dict:
        return {
            "table_name": self.table_name,
            "config": self.config,
            "player_profile": self.player_profile_dto.to_dict(),
            "top_winners": self.top_winners_dto.to_list(),
            "current_round": self.current_round_dto.to_dict()
        }
