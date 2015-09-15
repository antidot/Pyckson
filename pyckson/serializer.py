from pyckson.const import BASIC_TYPES
from pyckson.helpers import get_model
from pyckson.model import ListType


def serialize(obj):
    model = get_model(obj)
    result = {}
    for attribute in model.attributes:
        value = getattr(obj, attribute.python_name, None)
        if value is None and attribute.optional:
            continue
        elif value is None:
            raise ValueError('attribute {} of {} is None but not marked as optional'.format(attribute.python_name, obj))

        if attribute.attr_type in BASIC_TYPES:
            result[attribute.json_name] = value
        elif type(attribute.attr_type) is ListType:
            if attribute.attr_type.sub_type in BASIC_TYPES:
                list_result = value
            else:
                list_result = [serialize(sub_value) for sub_value in value]
            result[attribute.json_name] = list_result
        else:
            result[attribute.json_name] = serialize(value)
    return result
