
import json
from logger import Logger


class WSConnection:
    def __init__(self, data) -> None:
        self.player_id = data['player_id']
        self.client_id = data['client_id']
        self.websocket = data['websocket']
        self.connected_at = data['connected_at']

    async def send_message(self, data: dict) -> bool:
        try:
            await self.websocket.send(json.dumps(data))
            Logger.debug(f"Send message to player: {self.player_id} success")
            return True
        # except websockets.exceptions.ConnectionClosedError as ex:
        except Exception as ex:
            Logger.debug(f"Send message to player: {self.player_id} error. Error: {str(ex)}")
            return False
