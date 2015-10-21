from enum import Enum

from pyckson.const import BASIC_TYPES
from pyckson.helpers import get_model
from pyckson.model import ListType


def serialize_enum(cls, value):
    return value.name


def serialize_list(sub_type, value):
    return [serialize(sub_value) for sub_value in value]


def serialize_class(obj):
    model = get_model(obj)
    result = {}
    for attribute in model.attributes:
        value = getattr(obj, attribute.python_name, None)
        if value is None and attribute.optional:
            continue
        elif value is None:
            raise ValueError('attribute {} of {} is None but not marked as optional'.format(attribute.python_name, obj))
        elif type(attribute.attr_type) is ListType:
            result[attribute.json_name] = serialize_list(attribute.attr_type.sub_type, value)
        else:
            result[attribute.json_name] = serialize(value)
    return result


def serialize(obj):
    if obj.__class__ in BASIC_TYPES:
        return obj
    elif issubclass(obj.__class__, Enum):
        return serialize_enum(obj.__class__, obj)
    else:
        return serialize_class(obj)
