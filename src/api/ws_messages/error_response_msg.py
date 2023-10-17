import json

class ErrorResponseMsg:
    def __init__(self, err_msg: str) -> None:
        self.code = "error"
        self.error_message = err_msg
    
    def to_dict(self):
        return {
            'code': self.code,
            'error_message': self.error_message
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())