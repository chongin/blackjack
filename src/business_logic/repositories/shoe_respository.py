from data_models.shoe import Shoe
from api_clients.deck_card_api_client import DeckCardApiClient
from data_models.deck import Deck
from data_models.round import Round
from data_models.db_conn.firebase_client import FirebaseClient

class ShoeRepository:
    def __init__(self) -> None:
        pass

    def retrieve_shoe_model(self, shoe_name: str) -> Shoe:
        shoe_dict = FirebaseClient.instance().get_value(f"shoes/{shoe_name}")
        if shoe_dict is None:
            return None

        return Shoe(shoe_dict)
    
    def create_shoe_model(self, shoe_name: str, number_of_decks: int = 8) -> Shoe:
        deck_detail = DeckCardApiClient().create_new_deck(number_of_decks)
        print(f"create new deck: {deck_detail}")
        shoe_dm = Shoe.new_model(
            shoe_name, deck_detail.deck_api_id,
            number_of_decks
        )

        deck_dm = Deck.new_model(
            shoe_dm.shoe_id,
            shoe_dm.shuffer_count,
            deck_detail.deck_api_id,
            deck_detail.remain_card_count
        )

        round_dm = Round.new_model(deck_dm.deck_index)
        deck_dm.current_round = round_dm
        shoe_dm.current_deck = deck_dm

        return shoe_dm
    
    def save_shoe(self, shoe: Shoe) -> bool:
        FirebaseClient.instance().set_value(f"shoes/{shoe.shoe_name}", shoe.to_dict())
        print("save shoe success")
        return True