from pyckson.const import BASIC_TYPES
from pyckson.helpers import get_model
from pyckson.model import ListType


def parse(obj_type, json):
    model = get_model(obj_type)
    obj_args = {}
    for attribute in model.attributes:
        if attribute.json_name in json:
            value = json[attribute.json_name]
            if attribute.attr_type in BASIC_TYPES:
                obj_args[attribute.python_name] = value
            elif type(attribute.attr_type) is ListType:
                if attribute.attr_type.sub_type in BASIC_TYPES:
                    obj_args[attribute.python_name] = value
                else:
                    value = [parse(attribute.attr_type.sub_type, list_item) for list_item in value]
                    obj_args[attribute.python_name] = value
            else:
                obj_args[attribute.python_name] = parse(attribute.attr_type, value)
        elif attribute.optional:
            obj_args[attribute.python_name] = None
        else:
            raise ValueError('json is missing attribute {} to parse object {}'.format(attribute.json_name, obj_type))
    return obj_type(**obj_args)
