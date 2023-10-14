from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.flow_control.flow_state import FlowState
from logger import Logger
from abc import ABC, abstractmethod


class FlowBase:
    def __init__(self, job_data: dict) -> None:
        self.shoe_repository = ShoeRepository()
        self.shoe_name = job_data['shoe_name']
        self.round_id = job_data['round_id']
        self.context = {}

    def handle_flow(self) -> FlowState:
        if not self._do_validation():
            return FlowState.Fail_NotRetryable
        if not self._do_self_validation():
            return FlowState.Fail_NotRetryable
        
        if not self._process():
            return self.context['flow_state'] if self.context.get('flow_state') else FlowState.Fail_NotRetryable
        
        if not self._after_process():
            return FlowState.Fail_NotRetryable

    def _do_validation(self) -> bool:
        shoe = self.shoe_repository.retrieve_shoe_model(self.shoe_name)
        if shoe is None:
            Logger.error("Cannot find this shoe name", self.shoe_name)
            return False
        current_round = shoe.current_deck.current_round
        if self.round_id != current_round.round_id:
            Logger.error("Round id is not matched.", self.round_id,
                         current_round.round_id)
            return False
        self.context['current_round'] = current_round
        return True

    def _do_self_validation(self) -> bool:
        pass
    
    @abstractmethod
    def _process(self) -> bool:
        pass

    @abstractmethod
    def _after_process(self) -> bool:
        pass