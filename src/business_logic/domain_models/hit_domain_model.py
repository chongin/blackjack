from data_models.shoe import Shoe
from data_models.player_profile import PlayerProfile
from business_logic.domain_models.player_profile_dto import PlayerProfileDTO
from business_logic.domain_models.current_round_dto import CurrentRoundDTO


class HitDomainModel:
    def __init__(self, shoe: Shoe, player_profile: PlayerProfile) -> None:
        self.table_name = shoe.shoe_name
        self.player_profile_dto = PlayerProfileDTO.from_data_model(player_profile)
        self.current_round_dto = CurrentRoundDTO.from_data_model(shoe.current_deck.current_round)
        # it is important to filter current player data
        self.current_round_dto.filter_by_player_id(self.player_profile_dto.player_id)

    def to_dict(self) -> dict:
        return {
            "table_name": self.table_name,
            "player_profile": self.player_profile_dto.to_dict(),
            "current_round": self.current_round_dto.to_dict()
        }
