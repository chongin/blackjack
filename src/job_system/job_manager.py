import concurrent.futures
import time
import threading
from job_system.jobs.notify_job import *
from exceptions.system_exception import NotFoundException
from job_system.jobs.job_base import JobBase
from configuration.system_config import SystemConfig
from utils.util import Util


class JobManager:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init_manual__()
        return cls._instance

    def __init_manual__(self):
        self.excution_interval = SystemConfig.instance().check_job_timeout_interval_in_seconds
        self.jobs = []
        self.mutex = threading.Lock()
        pass
    
    def add_notify_bet_ended_job(self, job_data: dict) -> bool:
        print('add_notify_bet_ended_job', job_data)
        return self._add_job('NotifyBetEnded', job_data)
    
    def add_notify_closed_job(self, job_data: dict) -> bool:
        print('add_notify_closed_job', job_data)
        return self._add_job('NotifyClosedEnded', job_data)

    def add_notify_nex_round_opened_job(self, job_data: dict) -> bool:
        print('add_notify_nex_round_opened_job', job_data)
        return self._add_job('NotifyNextRoundOpened', job_data)
    
    def _add_job(self, job_type: str, job_data: dict) -> bool:
        job = None
        if job_type == 'NotifyBetEnded':
            job = NotifyBetEndedJob(job_data)
        elif job_type == 'NotifyClosedEnded':
            job = NotifyClosedEndedJob(job_data)
        elif job_type == 'NotifyNextRoundOpened':
            job = NotifyNextRoundOpened(job_data)
        else:
            raise NotFoundException(f"Cannot find this job type: {job_type}")
        
        self.mutex.acquire()
        self.jobs.add(job)
        self.mutex.release()
        
        return True
    
    def running(self):
        return True
    
    def start_timer(self):
        self.timer_task = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        # self.timer_task.submit(self.execute_timer)
        
    def execute_timer(self):
        while self.running():
            try:
                time.sleep(self.excution_interval)
                print(f"Excute timer run. {Util.current_utc_time()}")
                jobs = self.retrieve_timeout_jobs()
                print(jobs)
                if len(jobs) > 0:
                    self.handle_timeout_jobs(jobs)
            except Exception as e:
                print(f"Timer execution error: {e}")

    def retrieve_timeout_jobs(self):
        timeout_jobs = []

        self.mutex.acquire()
        for job in self.jobs:
            if job.is_expire():
                timeout_jobs.append(job)

        # remove timeout jobs from memory
        for time_out_job in timeout_jobs:
            for job in self.jobs:
                if time_out_job.job_id == job.job_id:
                    self.jobs.remove(job)
        self.mutex.release()
        return timeout_jobs
    
    def handle_timeout_jobs(self, timeout_jobs: list[JobBase]):
        # to find the control and handle it.
        # should update round state and brocast to all clients
        pass        