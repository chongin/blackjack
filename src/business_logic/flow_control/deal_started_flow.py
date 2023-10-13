from business_logic.flow_control.flow_state import FlowState
from api_clients.deck_card_api_client import DeckCardApiClient
from business_logic.repositories.shoe_respository import ShoeRepository
from logger import Logger
from data_models.card import Card

class DealStartedFlow:
    def __init__(self, job_data: dict) -> None:
        self.shoe_repository = ShoeRepository()
        self.shoe_name = job_data['shoe_name']
        self.round_id = job_data['round_id']
        self.player_id = job_data['player_id']
        self.context = {}
    
    def handle_deal_started(self) -> FlowState:
        # call api to draw card
        # update round state
        if not self._do_validation():
            return FlowState.Fail_NotRetryable

    def _process(self) -> FlowState:
        current_player_game_info = self.context['current_round']
        current_round = self.context['current_round']
        try:
            card_detail = DeckCardApiClient().draw_one_card(current_round.deck.deck_api_id)
        except Exception as ex:
            Logger.error(f"Call draw card api exception, error: {str(ex)}")
            return FlowState.Fail_Retryable
        
        card = Card({
            'code': card_detail.code,
            'value': card_detail.value,
            'suit': card_detail.suit
        })
        current_player_game_info.first_two_cards.append(card)

    def _do_validation(self) -> bool:
        shoe = self.shoe_repository.retrieve_shoe_model(self.shoe_name)
        if shoe is None:
            Logger.error("Cannot find this shoe name", self.shoe_name)
            return False
        
        current_round = shoe.current_deck.current_round
        if self.round_id != current_round.round_id:
            Logger.error("Round id is not matched.", self.round_id, current_round.round_id)
            return False
        
        if not current_round.is_bet_ended() or not current_round.is_deal_started():
            Logger.error("Round state is not matched", current_round.state)
            return False
        
        self.context['current_round'] = current_round
        if current_round.is_bet_ended():
            return self._validate_first_player_game_info()

        return self._validate_current_player_game_info()
    
    def _validate_first_player_game_info(self) -> bool:
        current_round = self.context['current_round']
        current_player_game_info = current_round.find_first_player_game_info()
        if not current_player_game_info:
            Logger.error(f"Cannot find first player game info. round state: {current_round.state}")
            return False
        
        count = len(current_player_game_info.first_two_cards)
        if count != 0:
            Logger.error(f"Player first two card sequence is not matche round state. player has {count} card. round state: {current_round.state}")
            return False
        
        self.context['current_player_game_info'] = current_player_game_info
        
        return True

    def _validate_current_player_game_info(self):
        current_round = self.context['current_round']
        deal_card_info = current_round['deal_card_info']
        if not deal_card_info.is_banker: 
            current_player_game_info = current_round.find_player_game_info_by_player_id(deal_card_info.player_id)
        else:
            current_player_game_info = current_round.banker_game_info

        if not current_player_game_info:
            Logger.error(f"Cannot find the match player game info. round state: {current_round.state}")
            return False
        
        count = len(current_player_game_info.first_two_cards)
        if count != current_round.deal_card_info.deal_card_index:
            Logger.error(f"Player:{deal_card_info.is_banker} first_two_card: {count}, but deal_card_info has: {current_round.deal_card_info.deal_card_index}")
            return False
        
        self.context['current_player_game_info'] = current_player_game_info
        return True