from aiworkflows.models.ai_task_primitive_type import AiTaskPrimitiveType, get_mapped_type
from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field


class AiTaskDataObject:
    def __init__(self,
                 obj_type: AiTaskPrimitiveType,
                 value=None,
                 message: str = None,
                 ):
        self.obj_type: AiTaskPrimitiveType = obj_type
        self.value = value
        self.message: str = message

    @staticmethod
    def from_json(json: dict) -> "AiTaskDataObject":
        obj_type = parse_required_field(json, 'type', AiTaskPrimitiveType)
        value = parse_optional_field(json, 'value', get_mapped_type(obj_type))
        message = parse_optional_field(json, 'message', str)

        return AiTaskDataObject(obj_type=obj_type,
                                value=value,
                                message=message)

    def to_json(self) -> dict:
        return {
            'type': self.obj_type.value,
            'value': self.value,
            'message': self.message,
        }

    def __repr__(self):
        return f'AiTaskDataObject(obj_type={self.obj_type}, value={self.value}, message={self.message})'

    def __str__(self):
        return self.__repr__()
