from exceptions.base_exception import BaseException


class SystemException(BaseException):
    def __init__(self, error_message="System raise error."):
        self.error_message = error_message
        super().__init__('System Error', 500, error_message)


class ConnectionNotFoundException(SystemException):
    def __init__(self, error_message):
        self.error_message = error_message
        super().__init__('Connection Not Found', 400, error_message)


class TimeoutException(SystemException):
    def __init__(self, error_message):
        super().__init__('Time Out', 400, error_message)


class RequestNotFoundException(SystemException):
    def __init__(self, error_message):
        super().__init__('Request Not Found', 400, error_message)