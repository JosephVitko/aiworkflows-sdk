from enum import Enum


class AiTaskPrimitiveType(Enum):
    """
    Enum for the primitive types of AI task data objects.
    """
    String = "String"
    Integer = "Integer"
    Float = "Float"
    Boolean = "Boolean"
    Dictionary = "Dictionary"
    List = "List"


# map from AiTaskPrimitiveType to Python type
_type_map: dict[AiTaskPrimitiveType, type] = {
    AiTaskPrimitiveType.String: str,
    AiTaskPrimitiveType.Integer: int,
    AiTaskPrimitiveType.Float: float,
    AiTaskPrimitiveType.Boolean: bool,
    AiTaskPrimitiveType.Dictionary: dict,
    AiTaskPrimitiveType.List: list
}


def get_mapped_type(obj_type: AiTaskPrimitiveType):
    """
    Gets the mapped Python type for the given AiTaskPrimitiveType.
    """
    if obj_type not in _type_map:
        raise ValueError(f"Error getting mapped type: AiTaskPrimitiveType {obj_type.value} has no type mapping")

    return _type_map[obj_type]
