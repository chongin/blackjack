from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.stand_domain_model import StandDomainModel
from exceptions.system_exception import *
from api_clients.authorization_api_client import AuthorizationApiClient


class StandBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
    
    def handle_stand(self, shoe_name: str, player_name: str, round_id: str) -> dict:
        # authen player:
        AuthorizationApiClient().validate_player({'player_name': player_name})

        # do validation
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
        
        #need to check player already stand or not
        

        #conver data to client
        return StandDomainModel(shoe, player_profile).to_dict()