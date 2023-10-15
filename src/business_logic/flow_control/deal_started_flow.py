from business_logic.flow_control.flow_state import FlowState
from api_clients.deck_card_api_client import DeckCardApiClient
from logger import Logger
from data_models.card import Card
from exceptions.system_exception import TimeoutException
from data_models.player_game_info import BankerGameInfo
from singleton_manger import SingletonManager
from business_logic.flow_control.game_rules.deal_card_rule import DealCardRule
from utils.util import Util
from business_logic.flow_control.flow_base import FlowBase


class DealStartedFlow(FlowBase):    
    def _do_self_validation(self) -> bool:
        current_round = self.context['current_round']
        if not current_round.is_bet_ended() and not current_round.is_deal_started():
            Logger.error("Round state is not matched", current_round.state)
            return False
        
        if len(current_round.deal_card_sequences) == 0:
            Logger.error("There is no player or banker need to deal card.")
            return False
        
        return True
    
    def _process(self) -> bool:
        if not self._get_current_player_game_info():
            return False
        if not self.check_player_can_deal_card():
            return False
        if not self.draw_one_card_from_server():
            return False

        self.assign_card_to_current_player_game_info()
        self._pop_up_current_player_id_from_deal_card_sequences()

        self._update_round_state()  # this should pup here after pop up card logic
        self._save_data()
        return True

    def _after_process(self) -> bool:
        self._broadcast_messages_to_clients()
        self._create_next_job()
        return True
    
    def check_player_can_deal_card(self) -> bool:
        current_player_game_info = self.context['current_player_game_info']
        return DealCardRule(current_player_game_info).can_deal()

    def draw_one_card_from_server(self) -> bool:
        current_round = self.context['current_round']
        try:
            card_detail = DeckCardApiClient().draw_one_card(current_round.deck.deck_api_id)
        except TimeoutException as ex:
            Logger.error(f"Call draw card api has timeout exception, error: {str(ex)}")
            self.context['flow_state'] = FlowState.Fail_Retryable
            return False
        except Exception as ex:
            Logger.error(f"Call draw card api exception, error: {str(ex)}")
            return False
        
        card = Card({
            'code': card_detail.code,
            'value': card_detail.value,
            'suit': card_detail.suit,
            'received_at': Util.current_utc_time()
        })

        self.context['card'] = card
        return True

    def _get_current_player_game_info(self) -> bool:
        current_round = self.context['current_round']
        # get current player id from the records
        current_player_id = current_round.deal_card_sequences[0]
        if current_player_id != BankerGameInfo.BANKER_ID:
            # this is deal to player, so get the player game info
            current_player_game_info = current_round.find_player_game_info_by_player_id(current_player_id)
            if not current_player_game_info:
                Logger.error("Cannot find the current player game info.", current_player_id)
                return False
            self.context['current_player_game_info'] = current_player_game_info
        else:
            # this is deal to banker, so get the banker game info
            self.context['current_player_game_info'] = current_round.banker_game_info
        return True
    
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
        SingletonManager.instance().connection_mgr.broadcast_message(message)

    def _create_next_job(self):
        current_round = self.context['current_round']
        if current_round.is_deal_started():
            SingletonManager.instance().job_mgr.add_notify_deal_started_job(current_round.notify_info())
        else:
            SingletonManager.instance().job_mgr.add_notify_deal_ended_job(current_round.notify_info())


