from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.bet_domain_model import BetDomainModel
from api.messages.components.bet_option_req import BetOptionsReq
from data_models.round import PlayerGameInfo
from data_models.bet_option import BetOption, BetOptions
from api_clients.authorization_api_client import AuthorizationApiClient
from api_clients.wallet_api_client import WalletApiClient
from exceptions.system_exception import *
from singleton_manger import SingletonManager
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
        
        if self.context['need_create_job']:
            self.create_bet_started_job()
        
        self.broadcast_bet_message_to_other_clients()
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
        
        player_game_info = current_round.find_player_game_info_by_player_id(player_profile.player_id)
        if not player_game_info:
            raise DataInvalidException(f"Cannot find this player in the player game info list. player_id: {player_profile.player_id}.")
        # later also need to validate the bet_options, because some bet_options has conditions, for example pair
        # validate_bet_options

        self.context.update({
            'shoe': shoe,
            'player_profile': player_profile,
            'current_round': current_round,
            'total_bet_amt': total_bet_amt,
            'player_game_info': player_game_info
        })
        
    def _process(self) -> None:
        self._add_bet_options_to_player_game_info()
        self._calculate_player_balance()
        self._update_round_status_to_bet_started()
        self._save_data()
        
    def _add_bet_options_to_player_game_info(self) -> None:
        bet_options_req = self.context['bet_options_req']
        player_game_info = self.context['player_game_info']
        # add data to data model object
        current_bet_options = BetOptions([])
        for bet_option_req in bet_options_req:
            current_bet_options.append(BetOption({
                "option_name": bet_option_req.option_name,
                "bet_amt": bet_option_req.bet_amt
            }))

        for bet_option in current_bet_options:
            player_game_info.bet_options.append(bet_option)
        
        self.context['current_bet_options'] = current_bet_options

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
            self.context['need_create_job'] = True
        else:
            self.context['need_create_job'] = False
    
    def _save_data(self) -> None:
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
        SingletonManager.instance().job_mgr.add_notify_bet_started_job(current_round.notify_info())

    def broadcast_bet_message_to_other_clients(self) -> None:
        player_profile = self.context['player_profile']
        current_bet_options = self.context['current_bet_options']
        current_round = self.context['current_round']

        message = {'action': 'notify_player_bet_options'}
        message.update(current_round.notify_info())
        message.update({
            'player_id': player_profile.player_id,
            'bet_options': current_bet_options.to_list()
        })
        SingletonManager.instance().connection_mgr.broadcase_messages_exclude_specifi_player(message, player_profile.player_id)