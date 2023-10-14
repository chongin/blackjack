from api.controllers.base_controller import BaseController
from business_logic.bet_business_logic import BetBusinessLogic


class BetController(BaseController):
    def __init__(self, request) -> None:
        super().__init__(request)

    def handle_request(self) -> dict:
        self.validate_request()

        return BetBusinessLogic().handle_bet(
            self.request.table_name,
            self.request.player_name,
            self.request.round_id,
            self.request.bet_options
        )
