from  controllers.base_controller import BaseController
from business_logic.hit_business_logic import HitBusinessLogic


class HitController(BaseController):
    def __init__(self, request) -> None:
        super().__init__(request)

    def handle_request(self) -> dict:
        self.validate_request()

        return HitBusinessLogic().handle_hit(
            self.request.table_name,
            self.request.player_name,
            self.request.round_id
        )
