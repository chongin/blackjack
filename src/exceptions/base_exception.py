class BaseException(Exception):
    def __init__(self, name, error_code, err_message):
        self.error_code = error_code
        self.err_message = err_message
        self.name = name
        super().__init__(f"Error Code: {error_code}, Message: {err_message}")

    def to_hash(self):
        return {
            "name": self.name,
            "error_code": self.error_code,
            "err_message": self.err_message
        }
