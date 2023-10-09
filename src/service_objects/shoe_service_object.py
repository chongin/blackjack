from data_models.shoe import Shoe
from data_models.deck import Deck
from data_models.round import Round
from api_clients.deck_card_api_client import DeckCardApiClient, DeckDetail
from ulid import ULID

class ShoeServiceObject:
    @classmethod
    def retrieve_shoe_object(cls, name: str) -> 'ShoeServiceObject':
        shoe_db = Shoe.retrieve_by_name(name)
        if shoe_db is None:
            shoe_db = cls.create_shoe_object(name, 8)

        return cls(shoe_db)
    
    @classmethod
    def create_shoe_object(cls, name: str, number_of_decks: int = 8) -> 'ShoeServiceObject':
        deck_detail = DeckCardApiClient().create_new_deck(number_of_decks)
        print(f"create new deck: {deck_detail}")
        shoe_db = Shoe.new_model(
            name, deck_detail.deck_api_id,
            number_of_decks
        )

        deck_db = Deck.new_model(
            shoe_db.shoe_id,
            shoe_db.shuffer_count,
            deck_detail.deck_api_id,
            deck_detail.remain_card_count
        )

        round_db = Round.new_model(deck_db.deck_index)
        deck_db.current_round = round_db
        shoe_db.current_deck = deck_db

        return cls(shoe_db)

    def __init__(self, shoe_db: Shoe) -> None:
        self.shoe_db = shoe_db

    def handle_query_game() -> None:
        pass