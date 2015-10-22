from enum import Enum

from pyckson.const import BASIC_TYPES, LIST_TYPES
from pyckson.helpers import get_model, is_base_type


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
        elif type(attribute.attr_type) in LIST_TYPES:
            result[attribute.json_name] = serialize_list(attribute.attr_type.sub_type, value)
        else:
            try:
                result[attribute.json_name] = serialize(value)
            except ValueError:
                raise ValueError('could not serialize field {} of {}, expected {}'.format(attribute.python_name,
                                                                                          obj.__class__.__name__,
                                                                                          attribute.attr_type.__name__))
    return result


def serialize(obj):
    if is_base_type(obj):
        return obj
    elif issubclass(obj.__class__, Enum):
        return serialize_enum(obj.__class__, obj)
    else:
        return serialize_class(obj)
