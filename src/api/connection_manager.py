import threading
from logger import Logger


class ConnectionManager:
    def __init__(self) -> None:
        self.connections = []
        self.mutex = threading.Lock()

    def broadcast_message(self, data: dict) -> bool:
        Logger.debug("Broadcase message success", data)
        return True
    
    def send_message_to_one_player(self, data: dict) -> bool:
        Logger.debug("send_message_to_one_player success", data)
        return True

    def broadcase_messages_exclude_specifi_player(self, data: dict, exclude_player_id: str) -> bool:
        Logger.debug(f"Broadcase message and exclude player: {exclude_player_id} success", data)
        return True