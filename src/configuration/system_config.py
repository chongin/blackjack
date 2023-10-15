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
            shoe = ShoeRepository().create_shoe_model(
                table['name'],
                number_of_decks,
                table['chips'],
                table['play_mode'],
                table['betting_countdown']
            )

            ShoeRepository().save_shoe(shoe)
