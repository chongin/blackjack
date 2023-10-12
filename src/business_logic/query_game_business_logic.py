from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.query_game_domain_model import QueryGameDomainModel
from api_clients.authorization_api_client import AuthorizationApiClient
from configuration.system_config import SystemConfig

class QueryGameBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
        self.context = {}

    def handle_query_game(self, shoe_name: str, player_name: str) -> None:
        self._do_validation(shoe_name, player_name)
        self._process()
        return self._compose_result()

    def _do_validation(self, shoe_name: str, player_name: str) -> None:
        # authen player:
        AuthorizationApiClient().validate_player({'player_name': player_name})

        # query data from db
        shoe = self.shoe_repository.retrieve_shoe_model(shoe_name)
        if shoe is None:
            shoe = self.shoe_repository.create_shoe_model(
                shoe_name,
                SystemConfig.instance().number_of_decks
            )
            self.context['need_save_shoe'] = True
           
        player_profile = self.player_profile_respository.retrieve_player_profile_model(player_name)
        if player_profile is None:
            player_profile = self.player_profile_respository.create_player_profile_model(player_name)
            self.context['need_save_profile'] = True

        self.context['shoe'] = shoe
        self.context['player_profile'] = player_profile

    def _process(self) -> None:
        need_save_shoe = self.context.get('need_save_shoe')
        need_save_profile = self.context.get('need_save_profile')
        
        # if have both, then need firebase transaction, how? 
        if need_save_shoe:
            shoe = self.context['shoe']
            self.shoe_repository.save_shoe(shoe)
        if need_save_profile:
            player_profile = self.context['player_profile']
            self.player_profile_respository.save_player(player_profile)

    def _compose_result(self) -> dict:
        # conver data to client
        player_profile = self.context['player_profile']
        shoe = self.context['shoe']
    
        top_winers = self.player_profile_respository.retrieve_top_winners(
            SystemConfig.instance().number_of_top_winners
        )

        return QueryGameDomainModel(shoe, player_profile, top_winers).to_dict()