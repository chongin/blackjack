from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository
from business_logic.domain_models.hit_domain_model import HitDomainModel
from exceptions.system_exception import *
from api_clients.authorization_api_client import AuthorizationApiClient
from business_logic.flow_control.game_rules.hit_card_rule import HitCardRule
from singleton_manger import SingletonManager
from api_clients.deck_card_api_client import DeckCardApiClient
from data_models.card import Card
from logger import Logger
from utils.util import Util


class HitBusinessLogic:
    def __init__(self) -> None:
        self.shoe_repository = ShoeRepository()
        self.player_profile_respository = PlayerProfileRespository()
        self.context = {}
    
    def handle_hit(self, shoe_name: str, player_name: str, round_id: str) -> dict:
        self._do_validation(shoe_name, player_name, round_id)
        self._process()
        if self.context['can_hit_more']:
            # just waitting current player to do next operation
            pass
        else:
            self._create_job_to_notify_next_player_or_banker_to_hit_or_stand()
        return self._compose_result()

    def _do_validation(self, shoe_name: str, player_name: str, round_id: str) -> None:
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
        
        if not current_round.can_interaction():
            raise BetNotAllowException(f"You cannot hit in this state of this Round id: {round_id}, state: {current_round.state}")
        
        player_game_info = current_round.find_player_game_info_by_player_id(player_profile.player_id)
        if not player_game_info:
            raise DataInvalidException(f"Cannot find this player in the player game info list. player_id: {player_profile.player_id}.")
        
        #  validate is this player can hit on this turn or not
        hit_card_sequences = current_round.deal_card_sequences
        if not hit_card_sequences or hit_card_sequences[0] != player_profile.player_id:
            raise ActionNotAllowedException(f"Base on play game sequence. It is not the turn for this player to hit. player_id: {player_profile.player_id}")

        #  validate can hit card or not
        if not HitCardRule(player_game_info).check_player_can_hit():
            raise ActionNotAllowedException(f"Base on game rule, this player cannot allow to hit now. player_id: {player_profile.player_id}")
        
        self.context.update({
            'player_profile': player_profile,
            'current_round': current_round,
            'player_game_info': player_game_info
        })

    def _process(self) -> None:
        self._draw_one_card_from_server()
        self._assign_card_player_game_info()
        if not self._check_player_can_hit_more():
            self._handle_player_hit_finished()  # cannot hit more
        else:
            self._handle_player_hit_more()
        self._save_data()

    def _draw_one_card_from_server(self) -> None:
        current_round = self.context['current_round']
        card_detail = DeckCardApiClient().draw_one_card(current_round.deck.deck_api_id)
        card = Card({
            'code': card_detail.code,
            'value': card_detail.value,
            'suit': card_detail.suit,
            'received_at': Util.current_utc_time()
        })

        self.context['card'] = card

    def _assign_card_player_game_info(self) -> None:
        player_game_info = self.context['player_game_info']
        card = self.context['card']
        player_game_info.hit_cards.append(card)
        Logger.debug(f"assign card to player, player_id: {player_game_info.player_id}", card)

    def _check_player_can_hit_more(self) -> bool:
        player_game_info = self.context['player_game_info']
        if not HitCardRule(player_game_info).check_player_can_hit():
            self.context['can_hit_more'] = False
        else:
            self.context['can_hit_more'] = True

    def _handle_player_hit_finished(self):
        player_game_info = self.context['player_game_info']
        player_game_info.is_stand = True
        self._popup_one_player_id_from_hit_cards()

    def _handle_player_hit_more(self):
        player_game_info = self.context['player_game_info']
        Logger.debug(f"This player:{player_game_info.player_id} can hit more card, waitting player next operation.")

    def _compose_result(self) -> dict:
        current_round = self.context['current_round']
        player_profile = self.context['player_profile']
        return HitDomainModel(current_round.deck.shoe, player_profile).to_dict()
    
    def _broadcast_hit_message_to_other_clients(self):
        player_profile = self.context['player_profile']
        current_round = self.context['current_round']

        message = {'action': 'notify_player_bet_options'}
        message.update(current_round.notify_info())
        message.update({
            'player_id': player_profile.player_id,
        })
        SingletonManager.instance().connection_mgr.broadcase_messages_exclude_specifi_player(message, player_profile.player_id)

    def _popup_one_player_id_from_hit_cards(self):
        current_round = self.context['current_round']
        pop_player_id = current_round.hit_card_sequences.pop(0)
        Logger.debug("Pop up player_id from hit card sequence", pop_player_id)

    def _save_data(self):
        current_round = self.context['current_round']
        self.shoe_repository.save_shoe(current_round.deck.shoe)

    def _create_job_to_notify_next_player_or_banker_to_hit_or_stand(self):
        current_round = self.context['current_round']
        SingletonManager.instance().job_mgr.add_notify_deal_ended_job(current_round.notify_info())