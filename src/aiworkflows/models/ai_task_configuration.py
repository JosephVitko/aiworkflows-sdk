from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field
from aiworkflows.models.ai_model_source import AiModelSource
from aiworkflows.models.ai_task_error_options import AiTaskErrorOptions


class AiTaskConfiguration:
    """
    Represents the configuration for an AI task.
    """

    def __init__(self,
                 model_id: str,
                 model_source: AiModelSource,
                 error_options: AiTaskErrorOptions,
                 additional_data: dict = None
                 ):
        """
        Initializes a new instance of the AiTaskConfiguration class.

        :param model_id: The ID of the model.
        :param model_source: The source of the model.
        :param error_options: The error options of the task.
        :param additional_data: The additional data of the task.
        """

        self.model_id: str = model_id
        self.model_source: AiModelSource = model_source
        self.error_options: AiTaskErrorOptions = error_options

        if additional_data is None:
            self.additional_data: dict = {}

        self.additional_data: dict = additional_data

    @staticmethod
    def from_json(json: dict) -> 'AiTaskConfiguration':
        """
        Creates a new instance of the AiTaskConfiguration class from a JSON object.

        :param json: The JSON object.
        """
        try:
            model_id: str = parse_required_field(json, 'modelId', str)
            model_source: AiModelSource = parse_required_field(json, 'modelSource', AiModelSource)
            error_options: AiTaskErrorOptions = parse_required_field(json, 'errorOptions', AiTaskErrorOptions)
            additional_data: dict = parse_optional_field(json, 'additionalData', dict, {})

            return AiTaskConfiguration(model_id, model_source, error_options, additional_data)
        except ValueError as e:
            raise ValueError(f'Cannot parse AiTaskConfiguration: {e}')

    def to_json(self) -> dict:
        """
        Converts the AiTaskConfiguration to a JSON object.
        """
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
