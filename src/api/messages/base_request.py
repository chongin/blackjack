from ulid import ULID
from abc import ABC, abstractmethod


class BaseRequest:
    def __init__(self, action: str) -> None:
        self.action = action
        self.request_id = str(ULID())
        
    def to_hash(self):
        return {
            "action": self.action,
            "request_id": self.request_id
        }

    @abstractmethod
    def validate() -> bool:
        pass