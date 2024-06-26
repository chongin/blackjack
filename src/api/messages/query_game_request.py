from api.messages.base_request import BaseRequest
from exceptions.system_exception import ParameterWrongException


class QueryGameRequest(BaseRequest):
    def __init__(self, data: dict) -> None:
        self.table_name = data.get('table_name')
        self.player_name = data.get('player_name')
        action_name = 'query_game'
        super().__init__(action_name)

    def validate(self) -> bool:
        if not self.table_name:
            raise ParameterWrongException("Table name was missed!")
        if not self.player_name:
            raise ParameterWrongException("Player name was missed!")
        return True
        

