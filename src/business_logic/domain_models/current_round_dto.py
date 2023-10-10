from data_models.round import Round
from data_models.deal_cards import PlayerCards, BankerCards
from data_models.result import Result
from business_logic.domain_models.deal_cards_dto import DealCardsDto, DealCardDto
from business_logic.domain_models.result_dto import ResultDTO, PlayerResultDTO


class CurrentRoundDTO:
    @classmethod
    def from_data_model(cls, round: Round) -> 'CurrentRoundDTO':
        return cls(
            round_id=round.round_id,
            state=round.state,
            hand=round.hand,
            player_cards=round.player_cards,
            banker_cards=round.banker_cards,
            result=round.result,
            has_black_card=round.has_black_card
        )

    def __init__(self, round_id: str, state: str, hand: int, player_cards: PlayerCards,
                 banker_cards: BankerCards, result: Result, has_black_card: bool) -> None:
        self.round_id = round_id
        self.state = state
        self.hand = hand
        self.player_cards = DealCardsDto.from_data_model(player_cards)
        self.banker_cards = DealCardsDto.from_data_model(banker_cards)

        # only have one banker, so change it to dict
        if len(self.banker_cards) > 0:
            self.banker_cards = self.banker_cards[0]
        else:
            self.banker_cards = {}

        self.result = ResultDTO.from_data_model(result)
        self.has_black_card = has_black_card

    def to_dict(self) -> dict:
        hash = {
            "round_id": self.round_id,
            "state": self.state,
            "hand": self.hand,
            "has_black_card": self.has_black_card
        }

        # it should be call filter_by_player_id first.
        if len(self.player_cards) > 0:
            hash["player_cards"] = self.player_cards.to_dict()
        else:
            hash["player_cards"] = {}
        
         # it should be call filter_by_player_id first.
        if len(self.banker_cards) > 0:
            hash["banker_cards"] = self.player_cards.to_dict()
        else:
            hash["banker_cards"] = {}

        # it should be call filter_by_player_id first.
        if type(self.result) is not dict:
            print(f"33333333333333 {self.player_cards}, {type(self.result)}")
            hash["result"] = self.result.to_dict()
        else:
            hash["result"] = {}

        return hash

    def filter_by_player_id(self, player_id: str):
        self.player_cards = self._filter_player_cards(player_id)
        if self.player_cards is None:
            self.player_cards = {}
        
        self.result = self._filter_result(player_id)
        if self.result is None:
            self.result = {}
        
    def _filter_player_cards(self, player_id: str):
        for deal_card_dto in self.player_cards:
            if deal_card_dto.player_id == player_id:
                return deal_card_dto
        return None
    
    def _filter_result(self, player_id: str):
        for player_result_dto in self.result:
            if player_result_dto.player_id == player_id:
                return player_result_dto
        return None