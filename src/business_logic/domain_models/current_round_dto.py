from data_models.round import Round
from data_models.deal_cards import PlayerCards, BankerCards
from data_models.result import Result
from business_logic.domain_models.deal_cards_dto import DealCardsDto
from business_logic.domain_models.result_dto import ResultDTO


class CurrentRoundDTO:
    @classmethod
    def from_data_model(cls, round: Round) -> 'CurrentRoundDTO':
        return cls(
            round_id=round.round_id,
            state=round.state,
            player_cards=round.player_cards,
            banker_cards=round.banker_cards,
            result=round.result,
            has_black_card=round.has_black_card
        )

    def __init__(self, round_id: str, state: str, player_cards: PlayerCards,
                 banker_cards: BankerCards, result: Result, has_black_card: bool) -> None:
        self.round_id = round_id
        self.state = state
        self.player_cards = DealCardsDto.from_data_model(player_cards)
        self.banker_cards = DealCardsDto.from_data_model(banker_cards)
        self.result = ResultDTO.from_data_model(result)
        self.has_black_card = has_black_card

    def to_dict(self) -> dict:
        return {
            "round_id": self.round_id,
            "state": self.state,
            "player_cards": self.player_cards.to_list(),
            "banker_cards": self.banker_cards.to_list(),
            "result": self.result.to_list(),
            "has_black_card": self.has_black_card
        }