from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.repositories.round_respository import RoundRepository
from business_logic.domain_models.bet_domain_model import BetDomainModel
from api.messages.components.bet_option_req import BetOptionsReq
from data_models.round import PlayerGameInfo
from data_models.bet_option import BetOption, BetOptions
from api_clients.authorization_api_client import AuthorizationApiClient
from api_clients.wallet_api_client import WalletApiClient
from exceptions.system_exception import *
from job_system.job_manager import JobManager
from api.connection_manager import ConnectionManager


class BetBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
        self.context = {}
    
    def handle_bet(self, shoe_name: str, player_name: str, round_id: str,
                   bet_options_req: BetOptionsReq) -> dict:
        
        self._do_validation(shoe_name, player_name, round_id, bet_options_req)
        self._process(bet_options_req)
        self._after_process()
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
        current_round = self.context['current_round']
        player_profile = self.context['player_profile']
        shoe = self.context['shoe']
        total_bet_amt = self.context['total_bet_amt']

        # add data to data model object
        bet_options = BetOptions([])
        for bet_option_req in bet_options_req:
            bet_options.append(BetOption({
                "option_name": bet_option_req.option_name,
                "bet_amt": bet_option_req.bet_amt
            }))

        round_repository = RoundRepository(current_round)
        player_game_info = round_repository.find_player_game_info_by_player_id(player_profile.player_id)
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

        # calculate player balance
        player_profile.deduct_balance(total_bet_amt)

        # call wallet api to deduct balance
        WalletApiClient().withdraw({
            'total_bet_amt': total_bet_amt,
            'player_id': player_profile.player_id
        })

        # update round status
        if current_round.is_opened():
            current_round.set_bet_started()
            self.context['need_notify'] = True
        else:
            self.context['need_notify'] = False

        # save data to db
        self.shoe_repository.save_shoe(shoe)
        self.player_profile_respository.save_player(player_profile)

    def _after_process(self) -> None:
        need_notify = self.context['need_notify']
        current_round = self.context['current_round']
        if need_notify:
            self._broadcast_message_to_clients(current_round)
            self.create_next_job(current_round)

    # conver data to client
    def _compose_result(self) -> dict:
        shoe = self.context['shoe']
        player_profile = self.context['player_profile']
        return BetDomainModel(shoe, player_profile).to_dict()

    # broadcase message through websocket
    def _broadcast_message_to_clients(self, current_round) -> None:
        message = {'action': 'notify_bet_started'}
        message.update(current_round.notify_info())
        message.update({'bet_started_at': current_round.bet_started_at})
        ConnectionManager.instance().broadcast_message(message)

    # createa next flow control job
    def create_next_job(self, current_round) -> None:
        JobManager.instance().add_notify_bet_ended_job(current_round.notify_info())