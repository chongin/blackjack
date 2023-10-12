
from data_models.round import Round
from business_logic.flow_control.flow_state import FlowState
from business_logic.repositories.shoe_respository import ShoeRepository
from logger import Logger
from api.connection_manager import ConnectionManager


class BetClosedFlow:
    def __init__(self, job_data: dict) -> None:
        self.shoe_repository = ShoeRepository()
        self.shoe_name = job_data['shoe_name']
        self.round_id = job_data['round_id']
        pass

    def handle_bet_closed(self) -> FlowState:
        # check need to update state or not
        # create the bet_ended job
        self._process()
        self._broadcast_message_to_clients(self.current_round)
        self.create_next_job(self.current_round)

    def _process(self) -> None:
        shoe = self.shoe_repository.retrieve_shoe_model(self.shoe_name)
        if shoe is None:
            Logger.error("Cannot find this shoe name", self.shoe_name)
            return FlowState.Fail_NonRetryable
        
        current_round = shoe.current_deck.current_round
        if self.round_id != current_round.round_id:
            Logger.error("Round id is not matched.", self.round_id, current_round.round_id)
            return FlowState.Fail_NonRetryable
        
        if not current_round.is_bet_started():
            Logger.error("Round state is not matched", current_round.state)
            return FlowState.Fail_NonRetryable
        
        current_round.set_bet_ended()
        self.shoe_repository.save_shoe(shoe)
        self.current_round = current_round

    def _broadcast_message_to_clients(self, current_round) -> None:
        message = {'action': 'notify_bet_closed'}
        message.update(current_round.notify_info())
        message.update({'bet_ended_at': current_round.bet_ended_at})
        ConnectionManager.instance().broadcast_message(message)

    def create_next_job(self, current_round) -> None:
        pass