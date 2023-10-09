from data_models.db_conn.firebase_client import FirebaseClient
from data_models.base_model import BaseModel
from data_models.deck import Deck
from data_models.deck_histories import DeckHistories


class ShoeConfig:
    def __init__(self, data) -> None:
        self.number_of_decks = data['number_of_decks']
        self.chips = data['chips']
        self.player_mode = data['player_mode']


class Shoe(BaseModel):
    @classmethod
    def retrieve_by_name(self, shoe_name: str):
        shoe_hash = FirebaseClient.instance().get_value(shoe_name)
        if shoe_hash is None:
            pass

        return Shoe(shoe_hash)
    
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.shoe_id = data['shoe_id']
        self.shoe_name = data['shoe_name']
        self.shuffer_count = data['shuffer_count']
        self.config = ShoeConfig(data['config'])
        self.deck_api_id = data['deck_api_id']
        self.state = data['state']
        self.current_deck = Deck(data['current_deck'])
        self.histories = DeckHistories(data['deck_histories'])

    def save(self):
        pass