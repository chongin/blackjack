from api_clients.api_client_base import ApiClientBase


class DeckDetail:
    def __init__(self, data: dict) -> None:
        self.deck_api_id = data['deck_id']
        self.shuffled = data['shuffled']
        self.remain_card_count = data['remaining']


class CardDetail:
    def __init__(self, data: dict) -> None:
        card_data = data.get('cards', [{}])[0]
        self.deck_api_id = data['deck_id']
        self.code = card_data.get('code', '')
        self.image = card_data.get('image', '')
        self.value = card_data.get('value', '')
        self.suit = card_data.get('suit', '')


class DeckCardApiClient(ApiClientBase):
    def __init__(self, endpoint='https://www.deckofcardsapi.com', timeout=10) -> None:
        super().__init__(endpoint, timeout)

    def create_new_deck(self, number_of_decks: int) -> DeckDetail:
        url_suffix = f"api/deck/new/shuffle?deck_count={number_of_decks}"
        data = self.make_request(url_suffix, "GET")
        return DeckDetail(data) if data else None

    def draw_one_card(self, deck_api_id: str) -> CardDetail:
        url_suffix = f"api/deck/{deck_api_id}/draw/?count=1"
        data = self.make_request(url_suffix, "GET")
        return CardDetail(data) if data else None


