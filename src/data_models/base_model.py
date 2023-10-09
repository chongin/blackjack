
class BaseModel:
    def __init__(self, data: dict) -> None:
        self.created_at = data['created_at']
        # self.updated_at = data['updated_at']
