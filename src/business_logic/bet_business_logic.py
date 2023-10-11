from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.bet_domain_model import BetDomainModel
from api.messages.components.bet_option_req import BetOptionsReq
from data_models.round import PlayerGameInfo
from data_models.bet_option import BetOption, BetOptions

from exceptions.system_exception import *


class BetBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
    
    def handle_bet(self, shoe_name: str, player_name: str, round_id: str,
                   bet_options_req: BetOptionsReq) -> dict:
        #do validation
        shoe_dm = self.shoe_repository.retrieve_shoe_model(shoe_name)
        if shoe_dm is None:
            raise TableNotFoundException(f"Cannot find this table: {shoe_name}")
        
        player_profile_dm = self.player_profile_respository.retrieve_player_profile_model(player_name)
        if player_profile_dm is None:
            raise PlayerNotFoundException(f"Cannot find this player: {player_name}")
        
        current_round_dm = shoe_dm.current_deck.current_round
        if current_round_dm.round_id != round_id:
            raise RoundNotFoundException(f"Round id: {round_id} is not matched current round. ")
        
        if not current_round_dm.can_bet():
            raise BetNotAllowException(f"You cannot bet in this state of this Round id: {round_id}, state: {current_round_dm.state}")
        
        total_bet_amt = bet_options_req.get_total_bet_amt()
        if total_bet_amt > player_profile_dm.wallet.balance:
            raise OverBalanceLimitException(f"You balance is {player_profile_dm.wallet.balance} is less than your total bet, cannot bet.")
        
        # add data to data model object
        bet_options_dm = BetOptions([])
        for bet_option_req in bet_options_req:
            bet_options_dm.append(BetOption({
                "option_name": bet_option_req.option_name,
                "bet_amt": bet_option_req.bet_amt
            }))

        player_game_info_dm = current_round_dm.find_player_game_info_by_player_id(player_profile_dm.player_id)
        if player_game_info_dm is None:
            player_game_info_dm = PlayerGameInfo({
                "player_id": player_profile_dm.player_id,
                "bet_options": bet_options_dm.to_list(),
                "first_two_cards": [],
                "hit_cards": [],
                "is_stand": False
            })
            current_round_dm.player_game_infos.append(player_game_info_dm)
        else:
            for bet_option_dm in bet_options_dm:
                player_game_info_dm.bet_options.append(bet_option_dm)

        # calculate player balance
        player_profile_dm.deduct_balance(total_bet_amt)

        # save data to db
        self.shoe_repository.save_shoe(shoe_dm)
        self.player_profile_respository.save_player(player_profile_dm)

        # conver data to client
        return BetDomainModel(shoe_dm, player_profile_dm).to_dict()