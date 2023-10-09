from data_models.db_conn.firebase_client import FirebaseClient
from data_models.base_model import BaseModel
from data_models.deck import Deck
from data_models.deck_histories import DeckHistories
from ulid import ULID

class ShoeConfig:
    def __init__(self, data) -> None:
        self.number_of_decks = data['number_of_decks']
        self.chips = data['chips']
        self.player_mode = data['player_mode']


class Shoe:
    @classmethod
    def retrieve_by_name(cls, shoe_name: str) -> 'Shoe':
        shoe_hash = FirebaseClient.instance().get_value(shoe_name)
        if shoe_hash is None:
            return None

        return Shoe(shoe_hash)
    
    @classmethod
    def new_model(cls, name: str, deck_api_id: str,
                  number_of_decks: int) -> 'Shoe':
        shoe_data = {
            'shoe_id': str(ULID()),
            'shoe_name': name,
            'shuffer_count': 0,
            'config': {
                "number_of_decks": number_of_decks,
                "chips": [1, 5, 10, 25, 50],
                "player_mode": "single"
            },
            'deck_api_id': deck_api_id,
            'state': 'active',
            'current_deck': None,
        }

        return cls(shoe_data)

    def __init__(self, data: dict) -> None:
        self.shoe_id = data['shoe_id']
        self.shoe_name = data['shoe_name']
        self.shuffer_count = data['shuffer_count']
        self.config = ShoeConfig(data['config'])
        self.deck_api_id = data['deck_api_id']
        self.state = data['state']
        self.current_deck = Deck(data['current_deck']) if data.get('current_deck') else None

    def save(self):
        pass