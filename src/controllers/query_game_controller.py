from controllers.base_controller import BaseController
from service_objects.shoe_service_object import ShoeServiceObject
from api.messages.query_game_request import QueryGameRequest
from service_objects.player_profile_service_object import PlayerProfileServiceObject

class QueryGameController(BaseController):
    def __init__(self, request: QueryGameRequest) -> None:
        super().__init__(request)

    def handle_request(self) -> dict:
        self.validate_request()
        shoe_obj = ShoeServiceObject.retrieve_shoe_object(
            self.request.table_name
        )

        player_obj = PlayerProfileServiceObject.retrieve_player_object(
            self.request.player_name
        )
        
        print(shoe_obj.shoe_db)
        return {"test": "success"}
