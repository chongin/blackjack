
from data_models.round import Round
from business_logic.flow_control.flow_state import FlowState
from business_logic.repositories.shoe_respository import ShoeRepository
from logger import Logger
from api.connection_manager import ConnectionManager
from job_system.job_manager import JobManager

class BetEndedFlow:
    def __init__(self, job_data: dict) -> None:
        self.shoe_repository = ShoeRepository()
        self.shoe_name = job_data['shoe_name']
        self.round_id = job_data['round_id']
        self.context = {}

    def handle_flow(self) -> FlowState:
        if not self._do_vaildation():
            return FlowState.Fail_NotRetryable
        
        self._process()
        self._broadcast_message_to_clients(self.current_round)
        self.create_deal_started_job()

    def _do_vaildation(self) -> bool:
        shoe = self.shoe_repository.retrieve_shoe_model(self.shoe_name)
        if shoe is None:
            Logger.error("Cannot find this shoe name", self.shoe_name)
            return False
        
        current_round = shoe.current_deck.current_round
        if self.round_id != current_round.round_id:
            Logger.error("Round id is not matched.", self.round_id, current_round.round_id)
            return False
        
        if not current_round.is_bet_started():
            Logger.error("Round state is not matched", current_round.state)
            return False
        
        self.context['current_round'] = current_round
        return True
        
    def _process(self) -> None:
        current_round = self.context['current_round']
        current_round.set_bet_ended()

        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def _broadcast_message_to_clients(self) -> None:
        current_round = self.context['current_round']
        message = {'action': 'notify_bet_closed'}
        message.update(current_round.notify_info())
        message.update({'bet_ended_at': current_round.bet_ended_at})
        ConnectionManager.instance().broadcast_message(message)

    def create_deal_started_job(self) -> None:
        current_round = self.context['current_round']
        JobManager.instance().add_notify_deal_started_job(current_round.notify_info())