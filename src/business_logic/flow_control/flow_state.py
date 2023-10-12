from enum import Enum, unique

@unique  # Ensure unique values
class FlowState(Enum):
    Success = 0
    Fail_Retryable = 1
    Fail_NonRetryable = 2
