import ulid import ULID


class RequestBase:
    def __init__(self, action: str) -> None:
        self.action = action
        self.request_id = str(ULID())
        
    def to_hash(self):
        return {
            "action": self.action,
            "request_id": self.request_id
        }