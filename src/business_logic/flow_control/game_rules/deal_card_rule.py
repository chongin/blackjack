from data_models.player_game_info import PlayerGameInfo


class DealCardRule:
    MAXIMUM_NUMBER_OF_DEAL_CARDS = 2

    def __init__(self, player_game_info: PlayerGameInfo) -> None:
        self.player_game_info = player_game_info

    def can_deal(self) -> bool:
        number_of_cards = len(self.player_game_info.first_two_cards)
        return number_of_cards < self.MAXIMUM_NUMBER_OF_DEAL_CARDS