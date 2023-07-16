from aiworkflows.compiler.utils.json_utils import parse_optional_field
from aiworkflows.models.ai_model_source import AiModelSource
from aiworkflows.models.ai_task_call_usage import AiTaskCallUsage
from aiworkflows.models.ai_task_data_object import AiTaskDataObject


class AiTaskCall:
    def __init__(self,
                 inputs: dict = None,
                 output: AiTaskDataObject = None,
                 model_id: str = None,
                 response_model_id: str = None,
                 model_source: AiModelSource = None,
                 success: bool = None,
                 timestamp: int = None,
                 task_id: str = None,
                 usage: AiTaskCallUsage = None,
                 ):
        self.inputs: dict = inputs
        self.output: AiTaskDataObject = output
        self.model_id: str = model_id
        self.response_model_id: str = response_model_id
        self.model_source: AiModelSource = model_source
        self.success: bool = success
        self.timestamp: int = timestamp
        self.task_id: str = task_id
        self.usage: AiTaskCallUsage = usage

    @staticmethod
    def from_json(json: dict) -> 'AiTaskCall':
        inputs = parse_optional_field(json, 'inputs', dict)
        output = parse_optional_field(json, 'output', AiTaskDataObject)
        model_id = parse_optional_field(json, 'model', str)
        response_model_id = parse_optional_field(json, 'responseModel', str)
        model_source = parse_optional_field(json, 'modelSource', AiModelSource)
        success = parse_optional_field(json, 'success', bool)
        timestamp = parse_optional_field(json, 'timestamp', int)
        task_id = parse_optional_field(json, 'taskId', str)
        usage = parse_optional_field(json, 'usage', AiTaskCallUsage)

        return AiTaskCall(inputs=inputs,
                          output=output,
                          model_id=model_id,
                          response_model_id=response_model_id,
                          model_source=model_source,
                          success=success,
                          timestamp=timestamp,
                          task_id=task_id,
                          usage=usage)

    def to_json(self):
        return {
            'inputs': self.inputs,
            'output': self.output,
            'model': self.model_id,
            'responseModel': self.response_model_id,
            'modelSource': self.model_source,
            'success': self.success,
            'timestamp': self.timestamp,
            'taskId': self.task_id,
            'usage': self.usage,
        }

    def __repr__(self):
        return f'AiTaskCall(inputs={self.inputs}, output={self.output}, model_id={self.model_id}, response_model_id={self.response_model_id}, model_source={self.model_source}, success={self.success}, timestamp={self.timestamp}, task_id={self.task_id}, usage={self.usage})'

    def __str__(self):
        return f'AiTaskCall(inputs={self.inputs}, output={self.output}, model_id={self.model_id}, response_model_id={self.response_model_id}, model_source={self.model_source}, success={self.success}, timestamp={self.timestamp}, task_id={self.task_id}, usage={self.usage})'