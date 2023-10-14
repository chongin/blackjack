from data_models.player_game_info import PlayerGameInfo


class HitCardRule:
    MUST_HIT_CARD_POINT = 17

    def __init__(self, player_game_info: PlayerGameInfo) -> None:
        self.player_game_info = player_game_info

    def check_player_can_hit(self):
        is_not_standing = not self.player_game_info.is_stand
        has_two_cards = len(self.player_game_info.first_two_cards) == 2
        is_not_bust = not self.player_game_info.is_bust()

        return is_not_standing and has_two_cards and is_not_bust

    def check_banker_can_hit(self):
        base_check = self.check_player_can_hit()
        if not base_check:
            return False
        
        if self.player_game_info.total_point() < self.MUST_HIT_CARD_POINT:
            return True
        
        return False