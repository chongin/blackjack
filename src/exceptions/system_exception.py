from exceptions.base_exception import SystemException

class ConnectionNotFoundException(SystemException):
    def __init__(self, error_message):
        self.error_message = error_message
        super().__init__(400, error_message)


class TimeoutException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class RequestNotFoundException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class ParameterWrongException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class TableNotFoundException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class PlayerNotFoundException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class RoundNotFoundException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class BetNotAllowException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class OverBalanceLimitException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)