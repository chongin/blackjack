from data_models.shoe import Shoe
from api_clients.deck_card_api_client import DeckCardApiClient
from data_models.deck import Deck
from data_models.round import Round
from data_models.db_conn.firebase_client import FirebaseClient
from logger import Logger


class ShoeRepository:
    def __init__(self) -> None:
        pass

    def retrieve_shoe_model(self, shoe_name: str) -> Shoe:
        shoe_dict = FirebaseClient.instance().get_value(f"shoes/{shoe_name}")
        if shoe_dict is None:
            return None

        return Shoe(shoe_dict)
    
    def create_shoe_model(self, shoe_name: str, number_of_decks: int,
                          chips: list[int], play_mode: str, betting_countdown: int) -> Shoe:
        deck_detail = DeckCardApiClient().create_new_deck(number_of_decks)
        print(f"create new deck: {deck_detail}")
        shoe = Shoe.new_model(
            shoe_name, deck_detail.deck_api_id,
            number_of_decks,
            chips,
            play_mode,
            betting_countdown
        )

        deck = Deck.new_model(
            shoe.shoe_id,
            shoe.shuffer_count,
            deck_detail.deck_api_id,
            deck_detail.remain_card_count
        )

        round = Round.new_model(deck.deck_index)
        round.set_parent(deck)

        deck.current_round = round
        deck.set_parent(shoe)

        shoe.current_deck = deck
        return shoe
 
    def save_shoe(self, shoe: Shoe) -> bool:
        FirebaseClient.instance().set_value(f"shoes/{shoe.shoe_name}", shoe.to_dict())
        Logger.debug(f"save shoe success: {shoe.shoe_name}")
        return True