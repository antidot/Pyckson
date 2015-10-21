from enum import Enum

from pyckson.const import BASIC_TYPES, LIST_TYPES
from pyckson.helpers import get_model, get_enum_parser


def parse_enum(cls, json):
    parser = get_enum_parser(cls)
    return parser.parse(json)


def parse_list(sub_type, json):
    return [parse(sub_type, sub_value) for sub_value in json]


def parse_class(cls, json):
    model = get_model(cls)
    obj_args = {}
    for attribute in model.attributes:
        if attribute.json_name in json:
            value = json[attribute.json_name]
            if type(attribute.attr_type) in LIST_TYPES:
                obj_args[attribute.python_name] = parse_list(attribute.attr_type.sub_type, value)
            else:
                obj_args[attribute.python_name] = parse(attribute.attr_type, value)
        elif not attribute.optional:
            raise ValueError('json is missing attribute {} to parse object {}'.format(attribute.json_name, cls))
    return cls(**obj_args)


def parse(cls, json):
    if cls in BASIC_TYPES:
        return json
    elif issubclass(cls, Enum):
        return parse_enum(cls, json)
    else:
        return parse_class(cls, json)
