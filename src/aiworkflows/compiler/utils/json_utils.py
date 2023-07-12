def parse_required_field(json: dict, field_name: str, field_type: type, default_value: any = None):
    """
    Parses a required field from a JSON object.
    :param json: The JSON object to parse from.
    :param field_name: The name of the field to parse.
    :param field_type: The type of the field to parse.
    :param default_value: The default value of the field to parse.
    :return: The parsed value.
    """
    if json is None:
        raise ValueError(f'Cannot parse {field_name}: json is None')

    if field_name not in json:
        if default_value is None:
            raise ValueError(f'Cannot parse {field_name}: json does not contain {field_name}')
        else:
            return default_value

    value: any
    try:
        if hasattr(field_type, 'from_json'):
            value = field_type.from_json(json[field_name])
        else:
            value = field_type(json[field_name])
    except ValueError:
        raise ValueError(f'Cannot parse {field_name}: {field_name} is not a valid {field_type.__name__}')

    return value


def parse_optional_field(json: dict, field_name: str, field_type: type, default_value: any = None):
    """
    Parses an optional field from a JSON object.
    :param json: The JSON object to parse from.
    :param field_name: The name of the field to parse.
    :param field_type: The type of the field to parse.
    :param default_value: The default value of the field to parse.
    :return: The parsed value.
    """
    if json is None:
        raise ValueError(f'Cannot parse {field_name}: json is None')

    if field_name not in json:
        return default_value

    if hasattr(field_type, 'from_json'):
        return field_type.from_json(json[field_name])

    field_value = json[field_name]
    if field_value is None:
        return default_value

    try:
        return field_type(field_value)
    except ValueError:
        raise ValueError(f'Cannot parse {field_name}: {field_name} is not a valid {field_type.__name__}')
