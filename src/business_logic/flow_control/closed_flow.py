from logger import Logger
from singleton_manger import SingletonManager
from utils.util import Util
from business_logic.flow_control.flow_base import FlowBase
from data_models.round import Round
from business_logic.repositories.round_histories_respository import RoundHistoriesRepository

class ClosedFlow(FlowBase):    
    def _do_self_validation(self) -> bool:
        current_round = self.context['current_round']
        if not current_round.is_resulted():
            Logger.error("Round state is not matched", current_round.state)
            return False
        return True

    def _process(self) -> bool:
        self._update_round_state_to_closed()
        self._save_round_to_history()
        self._generate_next_round()
        self._save_data()
        return True
    
    def _after_process(self) -> bool:
        self._broadcast_message_to_clients()
        return True
    
    def _generate_next_round(self) -> None:
        #  need to think about if there is a blackcard on this round
        current_round = self.context['current_round']
        current_deck = current_round.deck
        next_round = Round.new_model(current_round.deck_index)
        next_round.hand = current_round.hand + 1
        self.context['prev_round'] = current_round
        self.context['current_round'] = next_round
        current_deck.current_round = next_round
        next_round.set_parent(current_deck)

    def _save_round_to_history(self) -> None:
        current_round = self.context['current_round']
        RoundHistoriesRepository().save_round(current_round)

    def _update_round_state_to_closed(self) -> None:
        current_round = self.context['current_round']
        current_round.set_closed()

    def _save_data(self) -> None:
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def _broadcast_message_to_clients(self) -> None:
        prev_round = self.context['prev_round']
        current_round = self.context['current_round']

        message = {'action': 'notify_closed'}
        message.update(prev_round.notify_info())
        message.update({'next_round': current_round.notify_info()})
        SingletonManager.instance().connection_mgr.broadcast_message(message)