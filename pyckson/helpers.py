import re

from pyckson.const import PYCKSON_ATTR, PYCKSON_MODEL, PYCKSON_ENUM_PARSER, BASIC_TYPES, PYCKSON_NAMERULE
from pyckson.enum import EnumParser, DefaultEnumParser
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


def get_enum_parser(obj_or_class) -> EnumParser:
    if not hasattr(obj_or_class, PYCKSON_ENUM_PARSER):
        return DefaultEnumParser(obj_or_class)
    return getattr(obj_or_class, PYCKSON_ENUM_PARSER)


def is_base_type(obj):
    for btype in BASIC_TYPES:
        if isinstance(obj, btype):
            return True
    return False
