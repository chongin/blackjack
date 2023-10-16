
from logger import Logger
from singleton_manger import SingletonManager
from business_logic.flow_control.flow_base import FlowBase
from data_models.player_game_info import BankerGameInfo


class BetEndedFlow(FlowBase):
    def _do_self_validation(self) -> bool:
        current_round = self.context['current_round']
        if not current_round.is_bet_started():
            Logger.error("Round state is not matched", current_round.state)
            return False
        return True
        
    def _process(self) -> bool:
        self._create_deal_and_hit_card_sequence()
        self.set_state_to_bet_ended()
        self._save_data()
        return True

    def _after_process(self) -> bool:
        self._broadcast_message_to_clients()
        self.create_deal_started_job()
        return True

    def _broadcast_message_to_clients(self) -> None:
        current_round = self.context['current_round']
        message = {'action': 'notify_bet_ended'}
        message.update(current_round.notify_info())
        message.update({'bet_ended_at': current_round.bet_ended_at})
        SingletonManager.instance().connection_mgr.broadcast_message(message)

    def create_deal_started_job(self) -> None:
        current_round = self.context['current_round']
        SingletonManager.instance().job_mgr.add_notify_deal_started_job(current_round.notify_info())

    def set_state_to_bet_ended(self) -> None:
        current_round = self.context['current_round']
        current_round.set_bet_ended()

    def _save_data(self) -> None:
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def _create_deal_and_hit_card_sequence(self) -> None:
        current_round = self.context['current_round']
        bet_player_ids = current_round.get_all_player_id_have_betted()
       
        deal_card_sequences = []
        for i in range(2):
            for player_id in bet_player_ids:
                deal_card_sequences.append(player_id)
            
            deal_card_sequences.append(BankerGameInfo.BANKER_ID)

        hit_card_sequences = []
        for player_id in bet_player_ids:
            hit_card_sequences.append(player_id)
        hit_card_sequences.append(BankerGameInfo.BANKER_ID)

        current_round.deal_card_sequences = deal_card_sequences
        current_round.hit_card_sequences = hit_card_sequences
        Logger.info("add deal card sequences:", deal_card_sequences)
        Logger.info("add hit card sequences:", hit_card_sequences)