
from logger import Logger
from singleton_manger import SingletonManager
from business_logic.flow_control.flow_base import FlowBase


class BetEndedFlow(FlowBase):
    def _do_self_validation(self) -> bool:
        current_round = self.context['current_round']
        if not current_round.is_bet_started():
            Logger.error("Round state is not matched", current_round.state)
            return False
        return True
        
    def _process(self) -> bool:
        current_round = self.context['current_round']
        current_round.set_bet_ended()

        self.shoe_repository.save_shoe(current_round.deck.shoe)
        return True

    def _after_process(self) -> bool:
        self._broadcast_message_to_clients()
        self.create_deal_started_job()
        return True

    def _broadcast_message_to_clients(self) -> None:
        current_round = self.context['current_round']
        message = {'action': 'notify_bet_closed'}
        message.update(current_round.notify_info())
        message.update({'bet_ended_at': current_round.bet_ended_at})
        SingletonManager.instance().connection_mgr.broadcast_message(message)

    def create_deal_started_job(self) -> None:
        current_round = self.context['current_round']
        SingletonManager.instance().job_mgr.add_notify_deal_started_job(current_round.notify_info())