from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.query_game_domain_model import QueryGameDomainModel
from api_clients.authorization_api_client import AuthorizationApiClient
from configuration.system_config import SystemConfig
from exceptions.system_exception import TableNotFoundException
from data_models.player_game_info import PlayerGameInfo
from singleton_manger import SingletonManager
from logger import Logger

class QueryGameBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
        self.context = {}

    def handle_query_game(self, shoe_name: str, player_name: str) -> dict:
        self._do_validation(shoe_name, player_name)
        self._process()
        self._broadcast_new_player_message_to_other_clients()
        return self._compose_result()

    def _do_validation(self, shoe_name: str, player_name: str) -> None:
        # authen player:
        AuthorizationApiClient().validate_player({'player_name': player_name})

        # query data from db
        shoe = self.shoe_repository.retrieve_shoe_model(shoe_name)
        if shoe is None:
            raise TableNotFoundException(f"Cannot find this table: {shoe_name}")
           
        player_profile = self.player_profile_respository.retrieve_player_profile_model(player_name)
        if player_profile is None:
            player_profile = self.player_profile_respository.create_player_profile_model(player_name)
            self.context['new_player'] = True

        self.context['current_round'] = shoe.current_deck.current_round
        self.context['player_profile'] = player_profile

    def _process(self) -> None:
        if not self.context.get('new_player'):
            return
            
        self._handle_new_player_query_game()
        self._save_data()

    def _handle_new_player_query_game(self):
        current_round = self.context['current_round']
        player_profile = self.context['player_profile']

        new_player_game_info = PlayerGameInfo.generate_default_ins(player_profile.player_id)
        current_round.player_game_infos.append(new_player_game_info)
        Logger.debug("Add a new player to player game info list", new_player_game_info.to_dict())
    
    def _save_data(self):
        player_profile = self.context['player_profile']
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)
        self.player_profile_respository.save_player(player_profile)

    def _broadcast_new_player_message_to_other_clients(self):
        if not self.context.get('new_player'):
            return
        
        current_round = self.context['current_round']
        player_profile = self.context['player_profile']
        message = {'action': 'notify_new_player'}
        message.update(current_round.notify_info())
        SingletonManager.instance().connection_mgr.broadcase_messages_exclude_specifi_player(message, player_profile.player_id)

    def _compose_result(self) -> dict:
        # conver data to client
        player_profile = self.context['player_profile']
        current_round = self.context['current_round']
    
        top_winers = self.player_profile_respository.retrieve_top_winners(
            SystemConfig.instance().game_config['number_of_top_winners']
        )

        return QueryGameDomainModel(current_round.deck.shoe, player_profile, top_winers).to_dict()