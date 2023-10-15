from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.stand_domain_model import StandDomainModel
from exceptions.system_exception import *
from api_clients.authorization_api_client import AuthorizationApiClient
from business_logic.flow_control.game_rules.hit_card_rule import HitCardRule
from logger import Logger
from singleton_manger import SingletonManager


class StandBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
        self.context = {}
    
    def handle_stand(self, shoe_name: str, player_name: str, round_id: str) -> dict:
        self._do_validation(shoe_name, player_name, round_id)
        self._process()
        
        self._broadcast_stand_message_to_other_clients()
        self._create_job_to_notify_next_player_or_banker_to_hit_or_stand()

        return self._compose_result()
    
    def _do_validation(self, shoe_name: str, player_name: str, round_id: str) -> None:
        # authen player:
        AuthorizationApiClient().validate_player({'player_name': player_name})
        shoe = self.shoe_repository.retrieve_shoe_model(shoe_name)
        if shoe is None:
            raise TableNotFoundException(f"Cannot find this table: {shoe_name}")
        
        player_profile = self.player_profile_respository.retrieve_player_profile_model(player_name)
        if player_profile is None:
            raise PlayerNotFoundException(f"Cannot find this player: {player_name}")
        
        current_round = shoe.current_deck.current_round
        if current_round.round_id != round_id:
            raise RoundNotFoundException(f"Round id: {round_id} is not matched current round. ")
        
        if not current_round.can_interaction():
            raise BetNotAllowException(f"You cannot stand in this state of this Round id: {round_id}, state: {current_round.state}")
        
        player_game_info = current_round.find_player_game_info_by_player_id(player_profile.player_id)
        if not player_game_info:
            raise DataInvalidException(f"Cannot find this player in the player game info list. player_id: {player_profile.player_id}.")
        
        #  validate can stand or not
        if not HitCardRule(player_game_info).check_player_can_stand():
            raise ActionNotAllowedException(f"Base on game rule, this player cannot allow to hit now. player_id: {player_profile.player_id}")
        
        self.context.update({
            'player_profile': player_profile,
            'current_round': current_round,
            'player_game_info': player_game_info
        })

    def _process(self) -> None:
        self.update_player_hit_status()
        self._popup_one_player_id_from_hit_cards()
        self._save_data()

    def update_player_hit_status(self):
        player_game_info = self.context['player_game_info']
        player_game_info.is_stand = True
        Logger.debug(f"Update player: {player_game_info.player_id} status: is_stand = True")

    def _popup_one_player_id_from_hit_cards(self):
        current_round = self.context['current_round']
        pop_player_id = current_round.hit_card_sequences.pop(0)
        Logger.debug("Pop up player_id from hit card sequence", pop_player_id)

    def _save_data(self):
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def _create_job_to_notify_next_player_or_banker_to_hit_or_stand(self):
        current_round = self.context['current_round']
        SingletonManager.instance().job_mgr.add_notify_deal_ended_job(current_round.notify_info())

    def _compose_result(self) -> dict:
        current_round = self.context['current_round']
        player_profile = self.context['player_profile']
        return StandDomainModel(current_round.deck.shoe, player_profile).to_dict()
    
    def _broadcast_stand_message_to_other_clients(self):
        player_profile = self.context['player_profile']
        current_round = self.context['current_round']

        message = {'action': 'notify_player_stand'}
        message.update(current_round.notify_info())
        message.update({
            'player_id': player_profile.player_id,
        })
        SingletonManager.instance().connection_mgr.broadcase_messages_exclude_specifi_player(message, player_profile.player_id)
