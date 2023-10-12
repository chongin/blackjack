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

    def to_dict(self) -> dict:
        return {
            'number_of_decks': self.number_of_decks,
            'chips': self.chips,
            'player_mode': self.player_mode,
        }


class Shoe:
    @classmethod
    def retrieve_by_name(cls, shoe_name: str) -> 'Shoe':
        shoe_hash = FirebaseClient.instance().get_value(f"shoes/{shoe_name}")
        if shoe_hash is None:
            return None

        return cls(shoe_hash)
    
    @classmethod
    def new_model(cls, name: str, deck_api_id: str,
                  number_of_decks: int) -> 'Shoe':
        shoe_hash = {
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

        return cls(shoe_hash)

    def __init__(self, data: dict) -> None:
        self.shoe_id = data['shoe_id']
        self.shoe_name = data['shoe_name']
        self.shuffer_count = data['shuffer_count']
        self.config = ShoeConfig(data['config'])
        self.deck_api_id = data['deck_api_id']
        self.state = data['state']
        self.current_deck = Deck(data['current_deck']) if data.get('current_deck') else None
        if self.current_deck is not None:
            self.current_deck.set_parent(self)

    def notify_info(self) -> dict:
        return {
            'shoe_id': self.shoe_id,
            'shoe_name': self.shoe_name
        }
    
    def to_dict(self) -> dict:
        shoe_hash = {
            'shoe_id': self.shoe_id,
            'shoe_name': self.shoe_name,
            'shuffer_count': self.shuffer_count,
            'config': self.config.to_dict(),
            'deck_api_id': self.deck_api_id,
            'state': self.state,
        }

        if self.current_deck:
            shoe_hash['current_deck'] = self.current_deck.to_dict()

        return shoe_hash
