from controllers.base_controller import BaseController


class QueryGameController(BaseController):
    def __init__(self, request) -> None:
        super().__init__(request)

    def handle_request(self) -> dict:
        return {"query game": "success123123"}