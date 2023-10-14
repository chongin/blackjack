import threading
from logger import Logger


class ConnectionManager:
    def __init__(self) -> None:
        self.connections = []
        self.mutex = threading.Lock()

    def broadcast_message(self, data: dict) -> bool:
        Logger.info("Broadcase message success", data)
        return True
    
    def send_message_to_one_player(self, data: dict) -> bool:
        Logger.info("send_message_to_one_player success", data)
        return True
