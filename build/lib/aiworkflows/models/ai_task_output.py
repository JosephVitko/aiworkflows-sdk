from aiworkflows.models.ai_task_primitive_type import AiTaskPrimitiveType
from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field


class AiTaskOutput:
    def __init__(self,
                 output_type: AiTaskPrimitiveType,
                 name: str = None,
                 description: str = None,
                 parser_ref: str = None,
                 ):
        self.output_type: AiTaskPrimitiveType = output_type
        self.name: str = name
        self.description: str = description
        self.parser_ref: str = parser_ref

    @staticmethod
    def from_json(json: dict):
        output_type = parse_required_field(json, 'type', AiTaskPrimitiveType)
        name = parse_optional_field(json, 'name', str)
        description = parse_optional_field(json, 'description', str)
        parser_ref = parse_optional_field(json, 'parserRef', str)

        return AiTaskOutput(output_type=output_type,
                            name=name,
                            description=description,
                            parser_ref=parser_ref)

    def to_json(self):
        return {
            'type': self.output_type.value,
            'name': self.name,
            'description': self.description,
            'parserRef': self.parser_ref,
        }

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'AiTaskOutput(output_type={self.output_type}, name={self.name}, description={self.description}, parser_ref={self.parser_ref})'