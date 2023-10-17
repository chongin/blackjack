import threading
from logger import Logger
from api.ws_messages.register_msg import RegisterMsg
from logger import Logger
from api.connections.ws_connection import WSConnection
import asyncio

class ConnectionManager:
    def __init__(self) -> None:
        self.connections = {}
        self.mutex = threading.Lock()

    def handle_register(self, data: dict) -> str:
        try:
            register_msg = RegisterMsg(data)
            self._add_connection(WSConnection(register_msg.to_dict()))
            return "OK"
        except Exception as ex:
            Logger.error("handle register error. parameter data is:", data)
            return str(ex)

    def handle_message(self, data: dict) -> str:
        #  handle the notify messages response, need to check client received or not
        Logger.debug("Connection Manager is mocking handle this message success.", data)
        return "OK"

    def handle_disconnect(self, client_id: int) -> bool:
        pass

    def broadcast_message(self, data: dict) -> bool:
        Logger.debug("Begin to broadcase message")
        self.mutex.acquire()
        for _, connection in self.connections.items():
            res = asyncio.run(connection.send_message(data))
            if not res:
                Logger.error(f"Broadcase message to player:{connection.player_id} failed.", data)
                continue

        self.mutex.release()
        Logger.debug("Broadcase message success", data)
        
        return True
    
    def send_message_to_one_player(self, data: dict) -> bool:
        self.mutex.acquire()
        player_id = data['player_id']
        connection = self.connections.get(player_id)
        if not connection:
            Logger.error(f"Cannot find this player: {player_id} connection, cannot send this message:", data)
            self.mutex.release()
            return False
        
        res = asyncio.run(connection.send_message(data))
        if not res:
            Logger.error(f"Send message to one player: {player_id} failed.", data)
            self.mutex.release()
            return False
        
        self.mutex.release()
        Logger.debug("send_message_to_one_player success", data)
        return True

    def broadcase_messages_exclude_specifi_player(self, data: dict, exclude_player_id: str) -> bool:
        Logger.debug("Begin to broadcase message")
        self.mutex.acquire()
        for player_id, connection in self.connections.items():
            if player_id == exclude_player_id:
                Logger.debug(f"Exclude this player:{exclude_player_id}, don't need to send message:", data)
                continue
            res = asyncio.run(connection.send_message(data))
            if not res:
                Logger.error(f"In [broadcase_messages_exclude_specifi_player] brocast to player:{player_id} failed.", data)
                continue
        self.mutex.release()
        Logger.debug("Broadcase message success", data)
        return True

    def _add_connection(self, connection: WSConnection):
        self.mutex.acquire()
        self.connections[connection.player_id] = connection
        self.mutex.release()
        Logger.debug(f"Add connection success. player_id: {connection.player_id}")
