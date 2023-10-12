from job_system.jobs.job_base import JobBase
from configuration.system_config import SystemConfig


class NotifyBetEndedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data.update({
            "live_period_in_secondss": SystemConfig.get_job_timeout_in_seconds(self._get_class_name())
        }))

        self.bet_started_at = data['started_at']


class NotifyClosedEndedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data.update({
            "live_period_in_secondss": SystemConfig.get_job_timeout_in_seconds(self._get_class_name())
        }))


class NotifyNextRoundOpened(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data.update({
            "live_period_in_secondss": SystemConfig.get_job_timeout_in_seconds(self._get_class_name())
        }))
