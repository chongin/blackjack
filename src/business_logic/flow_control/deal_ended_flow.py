from business_logic.flow_control.flow_state import FlowState
from api_clients.deck_card_api_client import DeckCardApiClient
from logger import Logger
from data_models.card import Card
from data_models.player_game_info import BankerGameInfo
from singleton_manger import SingletonManager
from exceptions.system_exception import TimeoutException
from utils.util import Util
from business_logic.flow_control.game_rules.hit_card_rule import HitCardRule
from business_logic.flow_control.flow_base import FlowBase


class DealEndedFlow(FlowBase):    
    def _do_self_validation(self) -> bool:
        current_round = self.context['current_round']
        if not current_round.is_deal_ended():
            Logger.error("Round state is not matched", current_round.state)
            return False
        
        if len(current_round.hit_card_sequences) == 0:
            Logger.error("There is no player or banker need to deal card.")
            return False
        
        return True
    
    def _process(self) -> bool:
        if not self._get_current_player_game_info():
            return False
        
        if not self._check_can_hit():
            return False
        
        self.update_round_state_to_deal_ended()
        self.save_data()

        if not self.context['is_hit_by_player']:
            self._handle_banker_hit_card()
            self._check_banker_can_hit_more()  # check need to update is_stand or not
            self.save_data()
        return True

    def _after_process(self) -> bool:
        if self.context['is_hit_by_player']:
            self._notify_player_to_hit_card()
        else:
            self.broadcast_banker_hit_card_to_clients()

            current_player_game_info = self.context['current_player_game_info']
            current_round = self.context['current_round']
            # check if banker can hit more card or not
            if HitCardRule(current_player_game_info).check_banker_can_hit():
                SingletonManager.instance().job_mgr.add_notify_deal_ended_job(current_round.notify_info())
            else:
                SingletonManager.instance().job_mgr.add_notify_resulted_job(current_round.notify_info())
        return True

    def _get_current_player_game_info(self) -> bool:
        current_round = self.context['current_round']
        # get current player id from the records
        current_player_id = current_round.hit_card_sequences[0]
        if current_player_id != BankerGameInfo.BANKER_ID:
            # this is deal to player, so get the player game info
            current_player_game_info = current_round.find_player_game_info_by_player_id(current_player_id)
            if not current_player_game_info:
                Logger.error("Cannot find the current player game info.", current_player_id)
                return False
            self.context['current_player_game_info'] = current_player_game_info
            self.context['is_hit_by_player'] = True
        else:
            # this is deal to banker, so get the banker game info
            self.context['current_player_game_info'] = current_round.banker_game_info
            self.context['is_hit_by_player'] = False

        return True

    def _check_can_hit(self) -> bool:
        current_player_game_info = self.context['current_player_game_info']
        is_hit_by_player = self.context['is_hit_by_player']
        if is_hit_by_player:
            if not HitCardRule(current_player_game_info).check_player_can_hit():
                Logger.error(f"This player cannot hit card, {current_player_game_info.player_id}")
                return False
        else:
            if not HitCardRule(current_player_game_info).check_banker_can_hit():
                Logger.error(f"The banker cannot hit card, {current_player_game_info.player_id}")
                return False
        return True

    def _notify_player_to_hit_card(self) -> None:
        current_round = self.context['current_round']
        current_player_game_info = self.context['current_player_game_info']

        message = {'action': 'notify_hit_stand'}
        message.update(current_round.notify_info())
        message.update({
            'player_id': current_player_game_info.player_id
        })
        SingletonManager.instance().connection_mgr.send_message_to_one_player(message)
    
    def _handle_banker_hit_card(self) -> None:
        # draw one card
        self._draw_one_card_from_server()
        self.assign_card_to_banker_game_info()

    def _check_banker_can_hit_more(self) -> None:
        #  already check this player is a banker accroding the context
        current_player_game_info = self.context['current_player_game_info']
        if not HitCardRule(current_player_game_info).check_banker_can_hit():
            current_player_game_info.is_stand = True
            self._popup_one_player_id_from_hit_cards()

    def _popup_one_player_id_from_hit_cards(self):
        current_round = self.context['current_round']
        pop_player_id = current_round.hit_card_sequences.pop(0)
        Logger.debug("Pop up player_id from hit card sequence", pop_player_id, current_round.hit_card_sequences)

    def _draw_one_card_from_server(self) -> bool:
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
    
    def assign_card_to_banker_game_info(self) -> None:
        current_player_game_info = self.context['current_player_game_info']
        card = self.context['card']
        current_player_game_info.hit_cards.append(card)
        Logger.debug(f"assign car to banker, player_id: {current_player_game_info.player_id}, card: {card.to_dict()}")

    def update_round_state_to_deal_ended(self) -> None:
        current_round = self.context['current_round']
        current_round.set_deal_ended()

    def save_data(self) -> None:
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def broadcast_banker_hit_card_to_clients(self) -> None:
        current_round = self.context['current_round']
        card = self.context['card']

        message = {'action': 'notify_hit_card'}
        message.update(current_round.notify_info())
        message.update({'hit_to_banker': True})
        message.update({'card': card.to_dict()})
        SingletonManager.instance().connection_mgr.broadcast_message(message)