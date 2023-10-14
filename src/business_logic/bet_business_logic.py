from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.bet_domain_model import BetDomainModel
from api.messages.components.bet_option_req import BetOptionsReq
from data_models.round import PlayerGameInfo
from data_models.bet_option import BetOption, BetOptions
from api_clients.authorization_api_client import AuthorizationApiClient
from api_clients.wallet_api_client import WalletApiClient
from exceptions.system_exception import *
from job_system.job_manager import JobManager
from data_models.player_game_info import BankerGameInfo


class BetBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
        self.context = {}
    
    def handle_bet(self, shoe_name: str, player_name: str, round_id: str,
                   bet_options_req: BetOptionsReq) -> dict:
        self.context['bet_options_req'] = bet_options_req
        self._do_validation(shoe_name, player_name, round_id, bet_options_req)
        self._process()
        
        need_notify = self.context['need_notify']
        if need_notify:
            self.create_bet_started_job()
        return self._compose_result()

    def _do_validation(self, shoe_name: str, player_name: str, round_id: str,
                       bet_options_req: BetOptionsReq) -> None:
        # authen player:
        AuthorizationApiClient().validate_player({'player_name': player_name})

        # do validation
        shoe = self.shoe_repository.retrieve_shoe_model(shoe_name)
        if shoe is None:
            raise TableNotFoundException(f"Cannot find this table: {shoe_name}")
        
        player_profile = self.player_profile_respository.retrieve_player_profile_model(player_name)
        if player_profile is None:
            raise PlayerNotFoundException(f"Cannot find this player: {player_name}")
        
        current_round = shoe.current_deck.current_round
        if current_round.round_id != round_id:
            raise RoundNotFoundException(f"Round id: {round_id} is not matched current round. ")
        
        if not current_round.can_bet():
            raise BetNotAllowException(f"You cannot bet in this state of this Round id: {round_id}, state: {current_round.state}")
        
        total_bet_amt = bet_options_req.get_total_bet_amt()
        if total_bet_amt > player_profile.wallet.balance:
            raise OverBalanceLimitException(f"You balance is {player_profile.wallet.balance} is less than your total bet, cannot bet.")
        
        # later also need to validate the bet_options, because some bet_options has conditions, for example pair
        # validate_bet_options

        self.context.update({
            'shoe': shoe,
            'player_profile': player_profile,
            'current_round': current_round,
            'total_bet_amt': total_bet_amt
        })
        
    def _process(self, bet_options_req: BetOptionsReq) -> None:
        self._add_bet_options_to_player_game_info()
        self._calculate_player_balance()
        self._update_round_status_to_bet_started()
        self._create_deal_and_hit_card_sequence()
        self._save_data()
        
    def _add_bet_options_to_player_game_info(self) -> None:
        current_round = self.context['current_round']
        player_profile = self.context['player_profile']
        bet_options_req = self.context['bet_options_req']

        # add data to data model object
        bet_options = BetOptions([])
        for bet_option_req in bet_options_req:
            bet_options.append(BetOption({
                "option_name": bet_option_req.option_name,
                "bet_amt": bet_option_req.bet_amt
            }))

        player_game_info = current_round.find_player_game_info_by_player_id(player_profile.player_id)
        if player_game_info is None:
            player_game_info = PlayerGameInfo({
                "player_id": player_profile.player_id,
                "bet_options": bet_options.to_list(),
                "first_two_cards": [],
                "hit_cards": [],
                "is_stand": False
            })
            current_round.player_game_infos.append(player_game_info)
        else:
            for bet_option in bet_options:
                player_game_info.bet_options.append(bet_option)

    def _calculate_player_balance(self) -> None:
        player_profile = self.context['player_profile']
        total_bet_amt = self.context['total_bet_amt']

        player_profile.deduct_balance(total_bet_amt)
        # call wallet api to deduct balance
        WalletApiClient().withdraw({
            'total_bet_amt': total_bet_amt,
            'player_id': player_profile.player_id
        })

    def _update_round_status_to_bet_started(self) -> None:
        current_round = self.context['current_round']
        if current_round.is_opened():
            current_round.set_bet_started()
            self.context['need_notify'] = True
        else:
            self.context['need_notify'] = False

    def _create_deal_and_hit_card_sequence(self):
        need_notify = self.context['need_notify']
        if not need_notify:
            return
        
        current_round = self.context['current_round']
        bet_player_game_infos = current_round.get_all_player_id_have_betted()
        if len(bet_player_game_infos) == 0:
            raise DataInvalidException("Cannot find any player have betted, player bet data is wrong.")
        
        deal_card_sequences = []
        for i in range(2):
            for player_game_info in bet_player_game_infos:
                deal_card_sequences.append(player_game_info.player_id)
            
            deal_card_sequences.append(BankerGameInfo.BANKER_ID)

        hit_card_sequences = []
        for player_game_info in bet_player_game_infos:
            hit_card_sequences.append(player_game_info.player_id)
        hit_card_sequences.append(BankerGameInfo.BANKER_ID)

        current_round.deal_card_sequences = deal_card_sequences
        current_round.hit_card_sequences = hit_card_sequences
        
    def _save_data(self):
        shoe = self.context['shoe']
        player_profile = self.context['player_profile']
        self.shoe_repository.save_shoe(shoe)
        self.player_profile_respository.save_player(player_profile)

    # conver data to client
    def _compose_result(self) -> dict:
        shoe = self.context['shoe']
        player_profile = self.context['player_profile']
        return BetDomainModel(shoe, player_profile).to_dict()

    def create_bet_started_job(self) -> None:
        current_round = self.context['current_round']
        JobManager.instance().add_notify_bet_ended_job(current_round.notify_info())