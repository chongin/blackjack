from data_models.shoe import Shoe
from api_clients.deck_card_api_client import DeckCardApiClient


class ShoeServiceModel:
    @classmethod
    def retrieve_shoe(self, name: str):
        shoe_db = Shoe.retrieve_by_name(name)
        if shoe_db is None:
            shoe_db = self.create_shoe(8)

    @classmethod
    def create_shoe(self, number_of_decks=8) -> Shoe:
        deck_detail = DeckCardApiClient.create_new_deck(number_of_decks)

    def __init__(self) -> None:
        pass