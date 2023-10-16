from logger import Logger
from singleton_manger import SingletonManager
from business_logic.flow_control.flow_base import FlowBase


class BetStartedFlow(FlowBase):
    def _do_self_validation(self) -> bool:
        current_round = self.context['current_round'] 
        if not current_round.is_bet_started():
            Logger.error("Round state is not matched", current_round.state)
            return False
        return True
    
    def _process(self) -> bool:
        return True
    
    def _after_process(self) -> bool:
        self._broadcast_message_to_clients()
        self.create_bet_ended_job()
        return True

    def _save_data(self) -> None:
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def _broadcast_message_to_clients(self) -> None:
        current_round = self.context['current_round']
        message = {'action': 'notify_bet_started'}
        message.update(current_round.notify_info())
        message.update({
            'bet_started_at': current_round.bet_started_at,
            'count_down': 5  # need to calculate it TD
        })
        SingletonManager.instance().connection_mgr.broadcast_message(message)

    def create_bet_ended_job(self) -> None:
        current_round = self.context['current_round']
        # need to add a calculate the live time period TD
        SingletonManager.instance().job_mgr.add_notify_bet_ended_job(current_round.notify_info())