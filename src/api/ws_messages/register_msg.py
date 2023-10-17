from utils.util import Util


class RegisterMsg:
    def __init__(self, data: dict) -> None:
        self.player_id = data['player_id']
        self.shoe_name = data['table_name']
        self.client_id = data['client_id']
        self.websocket = data['websocket']
        self.connected_at = Util.current_utc_time()

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'shoe_name': self.shoe_name,
            'client_id': self.client_id,
            'websocket': self.websocket,
            'connected_at': self.connected_at
        }