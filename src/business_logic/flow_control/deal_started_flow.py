from business_logic.flow_control.flow_state import FlowState
from api_clients.deck_card_api_client import DeckCardApiClient
from business_logic.repositories.shoe_respository import ShoeRepository
from logger import Logger
from data_models.card import Card
from exceptions.system_exception import TimeoutException
from api.connection_manager import ConnectionManager


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

        self._process()
        self._after_process()

    def _process(self) -> FlowState:
        api_re = self.draw_one_card_from_server()
        if api_re != FlowState.Success:
            return api_re

        self.assign_card_to_current_player_game_info()
        self._pop_up_current_player_id_from_deal_card_sequences()
        self._save_data

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
        
        if len(current_round.deal_card_sequences) == 0:
            Logger.error("There is no player or banker need to deal card.")
            return False
        
        # get current player id from the records
        current_player_id = current_round.deal_card_sequences[0]
        if current_player_id != 'banker':
            # this is deal to player, so get the player game info
            current_player_game_info = round.find_player_game_info_by_player_id(current_player_id)
            if current_player_game_info == None:
                Logger.error("Cannot find the current player game info.", current_player_id)
                return False
            self.context['current_player_game_info'] = current_player_game_info
        else:
            # this is deal to banker, so get the banker game info
            self.context['current_player_game_info'] = round.banker_game_info
        self.context['current_round'] = current_round
        return True
    
    def draw_one_card_from_server(self) -> bool:
        current_round = self.context['current_round']
        try:
            card_detail = DeckCardApiClient().draw_one_card(current_round.deck.deck_api_id)
        except TimeoutException as ex:
            Logger.error(f"Call draw card api has timeout exception, error: {str(ex)}")
            return FlowState.Fail_Retryable
        except Exception as ex:
            Logger.error(f"Call draw card api exception, error: {str(ex)}")
            return FlowState.Fail_NotRetryable
        
        card = Card({
            'code': card_detail.code,
            'value': card_detail.value,
            'suit': card_detail.suit
        })

        self.context['card'] = card
        return FlowState.Success
    
    def assign_card_to_current_player_game_info(self) -> None:
        current_player_game_info = self.context['current_player_game_info']
        card = self.context['card']

        # assign it to player game info 
        current_player_game_info.first_two_cards.append(card)

    def _pop_up_current_player_id_from_deal_card_sequences(self):
        # pop up this player id from the deal_card_sequences
        current_round = self.context['current_round']
        pop_player_id = current_round.deal_card_sequences.pop(0)
        Logger.debug("Pop up player_id", pop_player_id)
        
    def _update_round_state(self):
        current_round = self.context['current_round']
        if len(current_round.deal_card_sequences) == 0:
            # already deal all cards
            current_round.set_deal_ended()
        else:
            current_round.set_deal_started()

    def _save_data(self):
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)
    
    def _broadcast_messages_to_clients(self):
        current_round = self.context['current_round']
        current_player_game_info = self.context['current_player_game_info']
        card = self.context['card']

        message = {'action': 'notify_deal_card'}
        message.update(current_round.notify_info())
        message.update({'deal_to_player': current_player_game_info.player_id})
        message.update({'card': card.to_dict()})
        ConnectionManager.instance().broadcast_message(message)


    def _create_next_job(self):
        current_round = self.context['current_round']
        if current_round.is_deal_started():
            current_round = self.context['current_round']
        else:
            
