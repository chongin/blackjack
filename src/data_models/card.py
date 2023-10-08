from data_models.base_model import BaseModel


class Card(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.round_id = data['round_id']
        self.hand = data['hand']
        self.card_code = data['card_code']
        self.value = data['value']
        self.suit = data['suit']
        self.received_at = data['received_at']
        self.image_url = self._compose_image_url()

    def _compose_image_url(self) -> str:
        return ""
    