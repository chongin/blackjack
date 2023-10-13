from api_clients.api_client_base import ApiClientBase


class DeckDetail:
    def __init__(self, data: dict) -> None:
        self.deck_api_id = data['deck_id']
        self.shuffled = data['shuffled']
        self.remain_card_count = data['remaining']


class CardDetail:
    def __init__(self, data: dict) -> None:
        self.deck_api_id = data['deck_id']
        self.code = data['code']
        self.image = data['image']
        self.value = data['value']
        self.suit = data['suit']


enable_mock = True
class DeckCardApiClient(ApiClientBase):
    def __init__(self, endpoint='https://www.deckofcardsapi.com', timeout=10) -> None:
        super().__init__(endpoint, timeout)

    def create_new_deck(self, number_of_decks: int) -> DeckDetail:
        global enable_mock
        if enable_mock:
            print("Mock create_new_deck...")
            return DeckDetail({
                "success": True,
                "deck_id": "3p40paa87x90",
                "shuffled": True,
                "remaining": 416
            })
        
        url_suffix = f"api/deck/new/shuffle?deck_count={number_of_decks}"
        data = self.make_request(url_suffix, "GET")
        return DeckDetail(data)

    def draw_one_card(self, deck_api_id: str) -> CardDetail:
        global enable_mock
        if enable_mock:
            print("Mock draw_one_card...")
            data = {
                "success": True, 
                "deck_id": "kxozasf3edqu",
                "cards": [
                    {
                        "code": "6H",
                        "image": "https://deckofcardsapi.com/static/img/6H.png",
                        "images": {
                                    "svg": "https://deckofcardsapi.com/static/img/6H.svg",
                                    "png": "https://deckofcardsapi.com/static/img/6H.png"
                                }, 
                        "value": "6",
                        "suit": "HEARTS"
                    },
                ],
                "remaining": 50
            }
            return CardDetail(data['cards'][0])

        url_suffix = f"api/deck/{deck_api_id}/draw/?count=1"
        data = self.make_request(url_suffix, "GET")
        return CardDetail(data['cards'][0])


