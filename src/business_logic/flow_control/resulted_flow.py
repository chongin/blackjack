from business_logic.flow_control.flow_state import FlowState
from logger import Logger
from data_models.card import Card
from data_models.player_game_info import BankerGameInfo, PlayerGameInfo
from singleton_manger import SingletonManager
from data_models.bet_option import BetOption
from utils.util import Util
from business_logic.flow_control.flow_base import FlowBase
from configuration.system_config import SystemConfig


class ResultedFlow(FlowBase):
    def _do_self_validation(self) -> bool:
        current_round = self.context['current_round']
        if not current_round.is_deal_ended():
            Logger.error("Round state is not matched", current_round.state)
            return False
        
        if len(current_round.hit_card_sequences) != 0:
            Logger.error("There is still have at least one player can do action, cannot calculate result now.")
            return False
        
        if not current_round.banker_game_info.is_stand:
            Logger.error("Banker is not stand, should wait for banker do action. .")
            return False
        
        return True
    
    def _process(self) -> bool:
        current_round = self.context['current_round']
        player_game_infos = current_round.get_all_player_info_have_betted()
        self.context['betted_player_game_infos'] = player_game_infos
        for player_game_info in player_game_infos:
            self._calculate_player_result(player_game_info)
        
        self.update_round_stauts()
        self._save_data()
        return True

    def _after_process(self) -> bool:
        self.broadcast_message_one_by_one()
        self._create_close_job()
        return True
    
    def _calculate_player_result(self, player_game_info: PlayerGameInfo) -> None:
        banker_game_info = self.context['current_round'].banker_game_info
        total_bet_amt = 0
        total_win_amt = 0
        for bet_option in player_game_info.bet_options:
            self._calculate_bet_option(
                player_game_info,
                player_game_info.total_point(),
                banker_game_info.total_point(),
                bet_option,
            )

            total_bet_amt += bet_option.bet_amt
            total_win_amt += bet_option.win_amt

        player_game_info.total_bet_amt = total_bet_amt
        player_game_info.total_win_amt = total_win_amt
        if player_game_info.total_win_amt > player_game_info.total_bet_amt:
            player_game_info.result = 'win'
        elif player_game_info.total_win_amt == player_game_info.total_bet_amt:
            player_game_info.result = 'draw'
        else:
            player_game_info.result = 'lost'

    def _calculate_bet_option(self, player_game_info: PlayerGameInfo, player_total_point: int,
                              banker_total_point: int, bet_option: BetOption) -> None: 
        odds = SystemConfig.instance().get_odd_by_option_name(bet_option.option_name)
        if bet_option.option_name == SystemConfig.instance().base_win_option_name():
            if player_total_point > banker_total_point:
                bet_option.result = 'win'
                if player_game_info.is_blackjack():
                    blackjack_odds = SystemConfig.instance().get_blackjack_odds
                    bet_option.win_amt = bet_option.bet_amt * blackjack_odds
                else:
                    bet_option.win_amt = bet_option.bet_amt * odds
            elif player_total_point == banker_total_point:
                bet_option.result = 'draw'
                bet_option.win_amt = (bet_option.bet_amt * odds) / 2
            else:
                bet_option.result = 'lost'  # TD should cacluate insurrence here
                bet_option.win_amt = 0
        elif bet_option.option_name == SystemConfig.instance().pair_option_name():
            first_card_value = player_game_info.first_two_cards[0].value
            second_card_value = player_game_info.first_two_cards[1].value
            if first_card_value == second_card_value:
                bet_option.result = 'win'
                bet_option.win_amt = bet_option.bet_amt * odds
            else:
                bet_option.result = 'lost'
                bet_option.win_amt = 0

    def update_round_stauts(self):
        current_round = self.context['current_round']
        current_round.set_resulted()
        Logger.debug(f"Update round state to {current_round.state}")

    def _save_data(self):
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def broadcast_message_one_by_one(self):
        player_game_infos = self.context['betted_player_game_infos']
        current_round = self.context['current_round']
        for player_game_info in player_game_infos:
            message = {'action': 'notify_resulted'}
            message.update(current_round.notify_info())
            message.update(player_game_info.to_dict())
            SingletonManager.instance().connection_mgr.send_message_to_one_player(message)

    def _create_close_job(self):
        current_round = self.context['current_round']
        SingletonManager.instance().job_mgr.add_notify_closed_job(current_round.notify_info())
