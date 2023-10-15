import os
import json
from business_logic.repositories.shoe_respository import ShoeRepository

class SystemConfig:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init_manual__()
        return cls._instance

    def __init_manual__(self) -> None:
        current_script_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_script_path)
        self.folder_path = f"{current_directory}/config"
        self._init_game_config()
        self._init_table_config()
        self._init_system_config()
    
    def _init_game_config(self) -> None:
        full_path = f"{self.folder_path}/game_config.json"
        with open(full_path, "r") as json_file:
            self.game_config = json.load(json_file)

    def _init_table_config(self) -> None:
        full_path = f"{self.folder_path}/table_config.json"
        with open(full_path, "r") as json_file:
            self.table_config = json.load(json_file)

    def _init_system_config(self) -> None:
        full_path = f"{self.folder_path}/system_config.json"
        with open(full_path, "r") as json_file:
            self.system_config = json.load(json_file)

    def get_job_timeout_in_milliseconds(self, job_name: str) -> int:
        return self.system_config['job_timeouts_in_millisec'][job_name]
    
    def set_tables(self) -> bool:
        number_of_decks = self.game_config['number_of_decks']
        for table in self.table_config['tables']:
            shoe = ShoeRepository().retrieve_shoe_model(table['name'])
            if shoe:
                continue
            
            shoe = ShoeRepository().create_shoe_model(
                table['name'],
                number_of_decks,
                table['chips'],
                table['play_mode'],
                table['betting_countdown']
            )

            ShoeRepository().save_shoe(shoe)

    def base_win_option_name(self):
        return self.game_config['bet_option_names'][0]

    def pair_option_name(self):
        return self.game_config['bet_option_names'][1]

    def insurence_option_name(self):
        return self.game_config['bet_option_names'][2]

    def double_down(self):
        return self.game_config['bet_option_names'][3]

    def get_odd_by_option_name(self, option_name: str):
        return self.game_config['odds'][option_name]
    
    def get_blackjack_odds(self):
        return self.game_config['odds']['blackjack']