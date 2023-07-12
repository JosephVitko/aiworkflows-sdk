from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field
from aiworkflows.models.ai_model_source import AiModelSource
from aiworkflows.models.ai_task_error_options import AiTaskErrorOptions


class AiTaskConfiguration:
    def __init__(self,
                 model_id: str,
                 model_source: AiModelSource,
                 error_options: AiTaskErrorOptions,
                 additional_data: dict = None
                 ):
        self.model_id: str = model_id
        self.model_source: AiModelSource = model_source
        self.error_options: AiTaskErrorOptions = error_options

        if additional_data is None:
            self.additional_data: dict = {}

        self.additional_data: dict = additional_data

    @staticmethod
    def from_json(json: dict):
        try:
            model_id: str = parse_required_field(json, 'modelId', str)
            model_source: AiModelSource = parse_required_field(json, 'modelSource', AiModelSource)
            error_options: AiTaskErrorOptions = parse_required_field(json, 'errorOptions', AiTaskErrorOptions)
            additional_data: dict = parse_optional_field(json, 'additionalData', dict, {})

            return AiTaskConfiguration(model_id, model_source, error_options, additional_data)
        except ValueError as e:
            raise ValueError(f'Cannot parse AiTaskConfiguration: {e}')

    def to_json(self):
        return {
            'modelId': self.model_id,
            'modelSource': self.model_source.value,
            'errorOptions': self.error_options.value,
            'additionalData': self.additional_data
        }

    def __repr__(self):
        return f'AiTaskConfiguration(model_id={self.model_id}, model_source={self.model_source}, ' \
               f'error_options={self.error_options}, additional_data={self.additional_data})'

    def __str__(self):
        return self.__repr__()
