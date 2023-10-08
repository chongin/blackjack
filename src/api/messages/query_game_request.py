#from api.messages.request_base import RequestBase

class QueryGameRequest:
    def __init__(self, data: dict) -> None:
        self.table_name = data.get('table_name')
        self.player_name = data.get('player_name')
        #action_name = 'query_game'
        #super().__init__(action_name)

    def validate() -> bool:
        return True
