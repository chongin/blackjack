from api.messages.base_request import BaseRequest
from exceptions.system_exception import ParameterWrongException


class StandRequest(BaseRequest):
    def __init__(self, data: dict) -> None:
        self.table_name = data.get('table_name')
        self.player_name = data.get('player_name')
        self.round_id = data.get('round_id')
        action_name = 'stand'
        super().__init__(action_name)

    def validate(self) -> bool:
        if not self.table_name:
            raise ParameterWrongException("Table name was missed!")
        if not self.player_name:
            raise ParameterWrongException("Player name was missed!")
        if not self.round_id:
            raise ParameterWrongException("Round ID was missed!")
        return True
