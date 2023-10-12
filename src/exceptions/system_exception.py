from exceptions.base_exception import SystemException

# Client need to handle exception start


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


# Client need to handle exception end 

# Backend raise exception, client need to raise a popup to show exception


class ParameterWrongException(SystemException):
    def __init__(self, error_message):
        super().__init__(400, error_message)


class NotFoundException(SystemException):
    def __init__(self, error_code, err_message):
        super().__init__(error_code, err_message)


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

# Backend exception ended.