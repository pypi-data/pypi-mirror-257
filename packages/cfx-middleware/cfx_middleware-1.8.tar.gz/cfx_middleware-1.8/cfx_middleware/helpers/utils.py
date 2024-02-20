import json
import sys

from cfx_middleware.classes.ParserResult import ParserResult


def to_camel_case(s):
    parts = s.split("_")
    return "".join(x.capitalize() for x in parts)


def convert_to_camel_case_dict(input_dict):
    output_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, dict):
            output_dict[to_camel_case(key)] = convert_to_camel_case_dict(value)
        elif isinstance(value, list):
            output_dict[to_camel_case(key)] = [
                convert_to_camel_case_dict(item) for item in value
            ]
        else:
            output_dict[to_camel_case(key)] = value
    return output_dict


def convert_to_dict(obj):
    if isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    elif hasattr(obj, "to_dict"):
        return convert_to_dict(obj.to_dict())
    else:
        return obj


def class_to_json(parser_result: ParserResult):
    attributes = vars(parser_result)
    data_converted = convert_to_camel_case_dict(convert_to_dict(attributes))

    del data_converted["Method"]

    return data_converted


def json_to_dict(variable):
    try:
        json_data = json.loads(variable)
        return json_data
    except json.JSONDecodeError as jsde:
        print("JSON Error:" + str(jsde))
        sys.exit(1)
