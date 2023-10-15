from api.controllers.base_controller import BaseController
from business_logic.stand_business_logic import StandBusinessLogic


class StandController(BaseController):
    def __init__(self, request) -> None:
        super().__init__(request)

    def handle_request(self) -> dict:
        self.validate_request()

        return StandBusinessLogic().handle_stand(
            self.request.table_name,
            self.request.player_name,
            self.request.round_id
        )
