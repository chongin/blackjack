from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.hit_domain_model import HitDomainModel
from api.messages.components.bet_option_req import BetOptionsReq
from data_models.round import Round, Result, PlayerGameInfo
from data_models.bet_option import BetOption, BetOptions

from exceptions.system_exception import *


class HitBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
    
    def handle_hit(self, shoe_name: str, player_name: str, round_id: str) -> dict:
        #do validation
        shoe_dm = self.shoe_repository.retrieve_shoe_model(shoe_name)
        if shoe_dm is None:
            raise TableNotFoundException(f"Cannot find this table: {shoe_name}")
        
        player_profile_dm = self.player_profile_respository.retrieve_player_profile_model(player_name)
        if player_profile_dm is None:
            raise PlayerNotFoundException(f"Cannot find this player: {player_name}")
        
        current_round_dm = shoe_dm.current_deck.current_round
        if current_round_dm.round_id != round_id:
            raise RoundNotFoundException(f"Round id: {round_id} is not matched current round. ")
        
        if not current_round_dm.can_interaction():
            raise BetNotAllowException(f"You cannot hit in this state of this Round id: {round_id}, state: {current_round_dm.state}")
        
        #need to check player already stand or not
        

        #conver data to client
        return HitDomainModel(shoe_dm, player_profile_dm).to_dict()