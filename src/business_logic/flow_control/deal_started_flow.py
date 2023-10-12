from business_logic.flow_control.flow_state import FlowState
from api_clients.deck_card_api_client import DeckCardApiClient
from business_logic.repositories.shoe_respository import ShoeRepository
from logger import Logger

class DealStartedFlow:
    def __init__(self, job_data: dict) -> None:
        self.shoe_repository = ShoeRepository()
        self.shoe_name = job_data['shoe_name']
        self.round_id = job_data['round_id']
        self.player_id = job_data['player_id']
    
    def handle_deal_started(self) -> FlowState:
        # call api to draw card
        # update round state

    def _process(self) -> None:
        shoe = self.shoe_repository.retrieve_shoe_model(self.shoe_name)
        if shoe is None:
            Logger.error("Cannot find this shoe name", self.shoe_name)
            return FlowState.Fail_NotRetryable
        
        current_round = shoe.current_deck.current_round
        if self.round_id != current_round.round_id:
            Logger.error("Round id is not matched.", self.round_id, current_round.round_id)
            return FlowState.Fail_NotRetryable
        
        if not current_round.is_bet_ended() or not current_round.is_deal_started():
            Logger.error("Round state is not matched", current_round.state)
            return FlowState.Fail_NotRetryable

