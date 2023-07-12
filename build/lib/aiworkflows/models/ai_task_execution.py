from aiworkflows.models.ai_task_call import AiTaskCall
from aiworkflows.models.ai_task_data_object import AiTaskDataObject
from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field


class AiTaskExecution:
    def __init__(self,
                 callstack: list[AiTaskCall],
                 result: AiTaskDataObject = None,
                 success: bool = None,
                 completion_timestamp: int = None,
                 ):
        self.callstack: list[AiTaskCall] = callstack
        self.result: AiTaskDataObject = result
        self.success: bool = success
        self.completion_timestamp: int = completion_timestamp

    @staticmethod
    def from_json(json: dict):
        callstack = parse_required_field(json, 'callStack', list)
        callstack = [AiTaskCall.from_json(c) for c in callstack]

        result = parse_optional_field(json, 'result', AiTaskDataObject)
        success = parse_optional_field(json, 'success', bool)
        completion_timestamp = parse_optional_field(json, 'completionTimestamp', int)

        return AiTaskExecution(callstack=callstack,
                               result=result,
                               success=success,
                               completion_timestamp=completion_timestamp)

    def to_json(self):

        callstack = [c.to_json() for c in self.callstack]

        return {
            'callStack': callstack,
            'result': self.result,
            'success': self.success,
            'completionTimestamp': self.completion_timestamp,
        }

    def __repr__(self):
        return f"AiTaskExecution(callstack={self.callstack}, result={self.result}, success={self.success}, completion_timestamp={self.completion_timestamp})"

    def __str__(self):
        return self.__repr__()