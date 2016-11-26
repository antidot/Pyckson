import re
import sys

from pyckson.const import PYCKSON_ATTR, PYCKSON_MODEL, BASIC_TYPES, PYCKSON_NAMERULE
from pyckson.model import PycksonModel


def is_pyckson(obj_type):
    return getattr(obj_type, PYCKSON_ATTR, False)


def get_model(obj_or_class) -> PycksonModel:
    if type(obj_or_class) is not type:
        return get_model(obj_or_class.__class__)
    if not is_pyckson(obj_or_class):
        raise ValueError('{} has no pyckson info'.format(obj_or_class))
    return getattr(obj_or_class, PYCKSON_MODEL)


def name_by_dict(name_mapping, default_rule):
    def name_function(python_name):
        if python_name in name_mapping:
            return name_mapping[python_name]
        else:
            return default_rule(python_name)

    return name_function


def camel_case_name(python_name):
    return re.sub('_([a-z])', lambda match: match.group(1).upper(), python_name)


def same_name(python_name):
    return python_name


def get_name_rule(obj_type):
    return getattr(obj_type, PYCKSON_NAMERULE, camel_case_name)


def is_base_type(obj):
    for btype in BASIC_TYPES:
        if isinstance(obj, btype):
            return True
    return False


class TypeProvider:
    def __init__(self, cls, name):
        self.cls = cls
        self.name = name

    def get(self):
        try:
            return getattr(sys.modules[self.cls.__module__], self.name)
        except AttributeError:
            raise TypeError('could not resolve string annotation {} in class {}'.format(self.name, self.cls.__name__))
