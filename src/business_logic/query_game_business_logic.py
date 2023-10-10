from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.query_game_domain_model import QueryGameDomainModel
from ulid import ULID


class QueryGameBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()

    def handle_query_game(self, shoe_name: str, player_name: str) -> None:
        shoe_dm = self.shoe_repository.retrieve_shoe_model(shoe_name)
        if shoe_dm is None:
            shoe_dm = self.shoe_repository.create_shoe_model(shoe_name, 8)
            self.shoe_repository.save_shoe(shoe_dm)
        
        player_profile_dm = self.player_profile_respository.retrieve_player_profile_model(player_name)
        if player_profile_dm is None:
            player_profile_dm = self.player_profile_respository.create_player_profile_model(player_name)
            self.player_profile_respository.save_player(player_profile_dm)

        top_winers_dm = self.player_profile_respository.retrieve_top_winners(5)

        return QueryGameDomainModel(shoe_dm, player_profile_dm, top_winers_dm).to_dict()


        
