import os
import json
from data_models.shoe import Shoe
from data_models.player_profile import PlayerProfile

from business_logic.repositories.shoe_respository import ShoeRepository
from business_logic.repositories.player_profile_respository import PlayerProfileRespository

class MockShareObj:
    def __init__(self, file_name, shoe_name='table1', player_name='chong') -> None:
        self.file_name = file_name
        self.shoe_name = shoe_name
        self.player_name = player_name
        self.data = self.load_data()
        self.player = self.create_player(self.data['players'][self.player_name])
        self.shoe = self.create_shoe(self.data['shoes'][self.shoe_name])

    def load_data(self):
        current_script_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_script_path)
        full_path = f"{current_directory}/test_datas/{self.file_name}.json"
        with open(full_path, "r") as json_file:
            json_data = json.load(json_file)

        return json_data

    def create_shoe(self, shoe_data):
        return Shoe(shoe_data)

    def create_player(self, player_data):
        return PlayerProfile(player_data)
    
    # for easily to test, set it to firebase. TD: should change the diffenent database name
    def save_to_firebase(self):
        ShoeRepository().save_shoe(self.shoe)
        PlayerProfileRespository().save_player(self.player)

    def retrieve_shoe_from_firebase(self):
        return ShoeRepository().retrieve_shoe_model(self.shoe_name)