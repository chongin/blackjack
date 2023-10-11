from api_clients.api_client_base import ApiClientBase

JOB_QUEUES = []


class JobQueueApi(ApiClientBase):
    def __init__(self, endpoint='https://www.mock_job_queue.com', timeout=10) -> None:
        super().__init__(endpoint, timeout)

    def read_jobs(self, jobs: list) -> list:
        global JOB_QUEUES
        return JOB_QUEUES

    def save_jobs(self, jobs: list) -> bool:
        global JOB_QUEUES
        for job in jobs:
            JOB_QUEUES.append(job)
        return True
    
    def add_job(self, job: dict) -> True:
        global JOB_QUEUES
        JOB_QUEUES.append(job)
        return True
