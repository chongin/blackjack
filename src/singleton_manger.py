from job_system.job_manager import JobManager

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
