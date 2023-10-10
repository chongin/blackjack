from api.messages.base_request import BaseRequest
from api.messages.components.bet_option_req import BetOptionsReq
from exceptions.system_exception import ParameterWrongException


class BetRequest(BaseRequest):
    def __init__(self, data: dict) -> None:
        self.table_name = data.get('table_name')
        self.player_name = data.get('player_name')
        self.round_id = data.get('round_id')
        self.bet_options = BetOptionsReq(data.get('bet_options')) if data.get('bet_options') else BetOptionsReq([])
        action_name = 'bet'
        super().__init__(action_name)

    def validate(self) -> bool:
        if not self.table_name:
            raise ParameterWrongException("Table name was missed!")
        if not self.player_name:
            raise ParameterWrongException("Player name was missed!")
        
        self.bet_options.validate()
        return True
