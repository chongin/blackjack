from job_system.job_manager import JobManager
from api.controller_factory import ControllerFactory
from api.message_factory import MessageFactory
from api.connection_manager import ConnectionManager

class SingletonManager:
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
        self.job_mgr = JobManager()
        self.control_factory = ControllerFactory()
        self.message_factory = MessageFactory()
        self.connection_mgr = ConnectionManager()