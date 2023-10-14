import threading
from logger import Logger


class ConnectionManager:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init_manual__()
        return cls._instance

    def __init_manual__(self) -> None:
        self.connections = []
        self.mutex = threading.Lock()

    def broadcast_message(self, data: dict) -> bool:
        Logger.info("Broadcase message success", data)
        return True
    
    def send_message_to_one_player(self, data: dict) -> bool:
        Logger.info("send_message_to_one_player success", data)
        return True
