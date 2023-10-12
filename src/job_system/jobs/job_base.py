from ulid import ULID
from utils.util import Util
from datetime import datetime, timedelta


class JobBase:
    def __init__(self, data: dict) -> None:
        self.job_id = str(ULID())
        self.job_name = self._get_class_name()
        self.shoe_id = data['shoe_name']
        self.round_id = data['round_id']
        self.round_state = data['state']
        self.live_period_in_seconds = data['live_period_in_secondss']
        self.expired_at = self.calculate_expire_time()
        self.created_at = Util.current_utc_time()

    def calculate_expire_time(self) -> str:
        expire_time = datetime.utcnow() + timedelta(seconds=self.live_period_in_seconds)
        return expire_time.strftime('%Y-%m-%dT%H:%M:%S')

    def is_expire(self) -> None:
        # '2023-10-12T02:29:34'
        expired_at_datetime = datetime.strptime(self.expired_at, '%Y-%m-%dT%H:%M:%S')
        return expired_at_datetime > datetime.utcnow()

    def _get_class_name(self) -> str:
        return self.__class__.__name__
