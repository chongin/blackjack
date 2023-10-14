from business_logic.flow_control.flow_state import FlowState
from api_clients.deck_card_api_client import DeckCardApiClient
from business_logic.repositories.shoe_respository import ShoeRepository
from logger import Logger
from data_models.card import Card
from api.connection_manager import ConnectionManager
from data_models.player_game_info import BankerGameInfo
from job_system.job_manager import JobManager
from exceptions.system_exception import TimeoutException
from utils.util import Util
from flow_control.game_rules.hit_card_rule import HitCardRule


class DealEndedFlow:
    def __init__(self, job_data: dict) -> None:
        self.shoe_repository = ShoeRepository()
        self.shoe_name = job_data['shoe_name']
        self.round_id = job_data['round_id']
        self.player_id = job_data['player_id']
        self.context = {}
    
    def handle_flow(self) -> FlowState:
        if not self._do_validation():
            return FlowState.Fail_NotRetryable
        
        if not self._process():
            return FlowState.Fail_NotRetryable

        if self.context['is_hit_by_player']:
            self._notify_player_to_hit_card()
        else:
            self.broadcast_banker_hit_card_to_clients()

            current_player_game_info = self.context['current_player_game_info']
            current_round = self.context['current_round']
            # check if banker can hit more card or not
            if HitCardRule(current_player_game_info).check_banker_can_hit():
                JobManager.add_notify_deal_ended_job(current_round.notify_info())
            else:
                JobManager.add_notify_resulted_job(current_round.notify_info())

    def _do_validation(self) -> bool:
        shoe = self.shoe_repository.retrieve_shoe_model(self.shoe_name)
        if shoe is None:
            Logger.error("Cannot find this shoe name", self.shoe_name)
            return False
        
        current_round = shoe.current_deck.current_round
        self.context['current_round'] = current_round
        if self.round_id != current_round.round_id:
            Logger.error("Round id is not matched.", self.round_id, current_round.round_id)
            return False
        
        if not current_round.is_deal_started():
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
            self.save_data()

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
        
        if self.context['current_player_game_info'].can_hit():
            Logger.error("Current player cannot hit card", current_player_game_info.to_dict())
            return False
        return True

    def _check_can_hit(self):
        current_player_game_info = self.context['current_player_game_info']
        is_hit_by_player = self.context['is_hit_by_player']
        if is_hit_by_player:
            return HitCardRule(current_player_game_info).check_player_can_hit()
        else:
            return HitCardRule(current_player_game_info).check_banker_can_hit()

    def _notify_player_to_hit_card(self):
        current_round = self.context['current_round']
        current_player_game_info = self.context['current_player_game_info']

        message = {'action': 'notify_hit_stand'}
        message.update(current_round.notify_info())
        message.update({
            'player_id': current_player_game_info.player_id
        })
        ConnectionManager.instance().send_message_to_one_player(message)
    
    def _handle_banker_hit_card(self):
        # draw one card
        self.draw_one_card_from_server()
        self.assign_card_to_banker_game_info()
 
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
    
    def assign_card_to_banker_game_info(self) -> None:
        current_player_game_info = self.context['current_player_game_info']
        card = self.context['card']
        current_player_game_info.hit_cards.append(card)

    def update_round_state_to_deal_ended(self):
        current_round = self.context['current_round']
        current_round.set_deal_ended()

    def save_data(self):
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def broadcast_banker_hit_card_to_clients(self):
        current_round = self.context['current_round']
        card = self.context['card']

        message = {'action': 'notify_hit_card'}
        message.update(current_round.notify_info())
        message.update({'hit_to_banker': True})
        message.update({'card': card.to_dict()})
        ConnectionManager.instance().broadcast_message(message)