from api.controllers.base_controller import BaseController
from api.messages.query_game_request import QueryGameRequest
from business_logic.query_game_business_logic import QueryGameBusinessLogic


class QueryGameController(BaseController):
    def __init__(self, request: QueryGameRequest) -> None:
        super().__init__(request)

    def handle_request(self) -> dict:
        self.validate_request()
        
        return QueryGameBusinessLogic().handle_query_game(self.request.table_name,
                                                          self.request.player_name)
