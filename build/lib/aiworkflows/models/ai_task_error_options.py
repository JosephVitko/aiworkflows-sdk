from enum import Enum


class AiTaskErrorOptions(Enum):
    """
    Enum for the options for handling errors in AI tasks.
    """
    Retry = "Retry"
    Fail = "Fail"
    Halt = "Halt"
