import threading


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

    def boardcast_message(self, data: dict) -> bool:
        pass
    


