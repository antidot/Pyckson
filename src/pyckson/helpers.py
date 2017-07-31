import re
import sys
from typing import _ForwardRef

from pyckson.const import PYCKSON_ATTR, BASIC_TYPES, PYCKSON_NAMERULE


def is_pyckson(obj_type):
    return getattr(obj_type, PYCKSON_ATTR, False)


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
        self.name = name.__forward_arg__ if type(name) is _ForwardRef else name

    def get(self):
        try:
            return getattr(sys.modules[self.cls.__module__], self.name)
        except AttributeError:
            raise TypeError('could not resolve string annotation {} in class {}'.format(self.name, self.cls.__name__))
