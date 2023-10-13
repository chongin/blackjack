from data_models.player_profile import PlayerProfile
from data_models.db_conn.firebase_client import FirebaseClient
from logger import Logger

class PlayerProfileRespository:
    def __init__(self) -> None:
        pass

    def retrieve_player_profile_model(self, player_name: str) -> PlayerProfile:
        player_profile_dict = FirebaseClient.instance().get_value(f"players/{player_name}")
        if player_profile_dict is None:
            return None

        return PlayerProfile(player_profile_dict)

    def create_player_profile_model(self, player_name: str) -> PlayerProfile:
        return PlayerProfile.new_model(player_name)

    def retrieve_top_winners(self, top_N: int) -> list[PlayerProfile]:
        all_player_profile_dict = FirebaseClient.instance().get_value("players")
        if not all_player_profile_dict:
            return []
        
        all_player_profiles = [PlayerProfile(data) for data in all_player_profile_dict.values()]
        sorted_profiles = sorted(all_player_profiles, key=lambda profile: profile.wallet.total_win, reverse=True)
        top_winners = sorted_profiles[:top_N]
        return top_winners
    
    def save_player(self, player: PlayerProfile) -> bool:
        FirebaseClient.instance().set_value(f"players/{player.player_name}", player.to_dict())
        Logger.debug(f"save player success, player_name: {player.player_name}, player_id: {player.player_id}")
        return True