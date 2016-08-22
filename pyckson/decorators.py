from enum import Enum

from pyckson.builders import PycksonModelBuilder
from pyckson.const import PYCKSON_TYPEINFO, PYCKSON_ATTR, PYCKSON_MODEL, PYCKSON_ENUM_PARSER, PYCKSON_NAMERULE
from pyckson.enum import CaseInsensitiveParser
from pyckson.helpers import same_name, name_by_dict, get_name_rule
from pyckson.parser import parse


def listtype(param_name, param_sub_type):
    def class_decorator(cls):
        type_info = getattr(cls, PYCKSON_TYPEINFO, dict())
        type_info[param_name] = param_sub_type
        setattr(cls, PYCKSON_TYPEINFO, type_info)
        return cls

    return class_decorator


def pyckson(cls):
    setattr(cls, PYCKSON_ATTR, True)
    model = PycksonModelBuilder(cls).build_model()
    setattr(cls, PYCKSON_MODEL, model)
    setattr(cls, 'parse', lambda json: parse(cls, json))
    return cls


def caseinsensitive(cls):
    if not issubclass(cls, Enum):
        raise TypeError('caseinsensitive decorator can only be applied to subclasses of enum.Enum')
    setattr(cls, PYCKSON_ENUM_PARSER, CaseInsensitiveParser(cls))
    return cls


def namerule(name_function):
    def class_decorator(cls):
        setattr(cls, PYCKSON_NAMERULE, name_function)
        return cls

    return class_decorator


def no_camel_case(cls):
    setattr(cls, PYCKSON_NAMERULE, same_name)
    return cls


def rename(**kwargs):
    def class_decorator(cls):
        name_function = name_by_dict(kwargs, get_name_rule(cls))
        setattr(cls, PYCKSON_NAMERULE, name_function)
        return cls

    return class_decorator
