import concurrent.futures
import time
import threading
from job_system.jobs.notify_job import *
from exceptions.system_exception import NotFoundException
from job_system.jobs.job_base import JobBase
from configuration.system_config import SystemConfig
from utils.util import Util
from logger import Logger
from business_logic.flow_control.flow_state import FlowState
from job_system.load_flow_modules import LoadFlowModules

class JobManager:
    def __init__(self) -> None:
        self.excution_interval = SystemConfig.instance().system_config['check_job_timeout_interval_in_millisec'] / 1000
        self.jobs = []
        self.mutex = threading.Lock()
        self.load_flow_modules = LoadFlowModules()

    def clear_jobs(self):
        self.mutex.acquire()
        self.jobs.clear()
        self.mutex.release()

    def add_notify_bet_started_job(self, job_data: dict) -> bool:
        return self._add_job('NotifyBetStartedJob', job_data)

    def add_notify_bet_ended_job(self, job_data: dict) -> bool:
        return self._add_job('NotifyBetEndedJob', job_data)
    
    def add_notify_deal_started_job(self, job_data: dict) -> bool:
        return self._add_job('NotifyDealStartedJob', job_data)

    def add_notify_deal_ended_job(self, job_data: dict) -> bool:
        return self._add_job('NotifyDealEndedJob', job_data)
    
    def add_notify_resulted_job(self, job_data: dict) -> bool:
        return self._add_job('NotifyResultedJob', job_data)
    
    def add_notify_closed_job(self, job_data: dict) -> bool:
        return self._add_job('NotifyClosedJob', job_data)

    def _add_job(self, job_name: str, job_data: dict) -> bool:
        job = None
        if job_name == 'NotifyBetStartedJob':
            job = NotifyBetStartedJob(job_data)
        elif job_name == 'NotifyBetEndedJob':
            job = NotifyBetEndedJob(job_data)
        elif job_name == 'NotifyDealStartedJob':
            job = NotifyDealStartedJob(job_data)
        elif job_name == 'NotifyDealEndedJob':
            job = NotifyDealEndedJob(job_data)
        elif job_name == 'NotifyResultedJob':
            job = NotifyResultedJob(job_data)
        elif job_name == 'NotifyClosedJob':
            job = NotifyClosedJob(job_data)
        else:
            raise NotFoundException(f"Cannot find this job name: {job_name}")
        
        Logger.debug("Add a job to job system.", job.to_dict())
        self.mutex.acquire()
        self.jobs.append(job)
        self.mutex.release()
        
        return True
    
    def running(self) -> bool:
        return True
    
    def start_timer(self) -> None:
        self.timer_task = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.timer_task.submit(self.execute_timer)
        
    def execute_timer(self) -> None:
        while self.running():
            try:
                time.sleep(self.excution_interval)
                print(f"Excute timer run. {Util.current_utc_time()}")
                timeout_jobs = self.retrieve_timeout_jobs()
                for timeout_job in timeout_jobs:
                    self.handle_timeout_job(timeout_job)
            except Exception as e:
                print(f"Timer execution error: {e}")

    def retrieve_timeout_jobs(self) -> list[JobBase]:
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

    def handle_timeout_job(self, job: JobBase) -> None:
        Logger.debug("Start to handle timeout job:", job.to_dict())
        
        flow_name = job.job_name.replace("Notify", "").replace("Job", "")
        flow_name = Util.camelcase_to_underscore(flow_name)

        flow = self.load_flow_modules.create_flow(flow_name, job.to_dict())
        ret = flow.handle_flow()
        
        if ret == FlowState.Fail_Retryable:
            job.live_period_in_milliseconds = 3000
            job.expired_at = job.calculate_expire_time()
            self.mutex.acquire()
            self.jobs.append(job)
            self.mutex.release()
            Logger.debug("Add a retryable job to queue again. try it later.", job.to_dict())
        elif ret == FlowState.Fail_NotRetryable:
            Logger.error("Execute this job failed and not retryable, need to manual handle it.", job.to_dict())
        else:
            Logger.info("Excute job successfull.", job.to_dict())

    

    