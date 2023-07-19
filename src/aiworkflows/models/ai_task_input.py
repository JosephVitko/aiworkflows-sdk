from aiworkflows.models.ai_task_primitive_type import AiTaskPrimitiveType
from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field


class AiTaskInput:
    """
    Defines an input for an AI task.
    """
    def __init__(self,
                 input_type: AiTaskPrimitiveType,
                 input_ref: str,
                 input_name: str = None,
                 input_description: str = None,
                 is_required: bool = True,
                 ):
        """
        Initializes a new instance of the AiTaskInput class.

        :param input_type: The type of the input.
        :param input_ref: The reference to the input.
        :param input_name: The human-readable name of the input.
        :param input_description: The human-readable description of the input.
        :param is_required: Indicates whether the input is required.
        """
        self.input_type: AiTaskPrimitiveType = input_type
        self.input_ref: str = input_ref
        self.input_name: str = input_name
        self.input_description: str = input_description
        self.is_required: bool = is_required

    @staticmethod
    def from_json(json: dict) -> "AiTaskInput":
        """
        Creates a new instance of the AiTaskInput class from a JSON object.

        :param json: The JSON object.
        """
        input_type = parse_required_field(json, 'type', AiTaskPrimitiveType)
        input_ref = parse_required_field(json, 'inputRef', str)
        input_name = parse_optional_field(json, 'name', str)
        input_description = parse_optional_field(json, 'description', str)
        is_required = parse_optional_field(json, 'isRequired', bool, True)

        return AiTaskInput(input_type=input_type,
                           input_ref=input_ref,
                           input_name=input_name,
                           input_description=input_description,
                           is_required=is_required)

    def to_json(self) -> dict:
        """
        Creates a JSON object from the AiTaskInput object.
        """
        return {
            'type': self.input_type.value,
            'inputRef': self.input_ref,
            'name': self.input_name,
            'description': self.input_description,
            'isRequired': self.is_required,
        }

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'AiTaskInput(input_type={self.input_type}, input_ref={self.input_ref}, input_name={self.input_name}, input_description={self.input_description}, is_required={self.is_required})'
