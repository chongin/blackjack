from data_models.player_profile import PlayerProfile


class PlayerProfileServiceObject:
    @classmethod
    def retrieve_player_object(cls, name: str) -> 'PlayerProfileServiceObject':
        player_profle_db = PlayerProfile.retrieve_by_name(name)
        if player_profle_db is None:
            player_profle_db = cls.create_player_profile_object(name)

        return cls(player_profle_db)
    
    def __init__(self, player_profle_db: PlayerProfile) -> None:
        pass