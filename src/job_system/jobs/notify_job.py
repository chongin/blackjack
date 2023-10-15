from job_system.jobs.job_base import JobBase
from configuration.system_config import SystemConfig


class NotifyBetStartedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.bet_started_at = data['bet_started_at']

    def to_dict(self):
        hash = super().to_dict()
        hash.update({'bet_started_at': self.bet_started_at})
        return hash


class NotifyBetEndedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data)


class NotifyDealStartedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data)


class NotifyDealEndedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data)


class NotifyResultedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data)


class NotifyClosedJob(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data)


class NotifyNextRoundOpened(JobBase):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
