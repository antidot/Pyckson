import re

from pyckson.enum import EnumParser, DefaultEnumParser
from pyckson.model import PycksonModel
from pyckson.const import PYCKSON_ATTR, PYCKSON_MODEL, PYCKSON_ENUM_PARSER


def is_pyckson(obj_type):
    return getattr(obj_type, PYCKSON_ATTR, False)


def get_model(obj_or_class) -> PycksonModel:
    if type(obj_or_class) is not type:
        return get_model(obj_or_class.__class__)
    if not is_pyckson(obj_or_class):
        raise ValueError('{} has no pyckson info'.format(obj_or_class))
    return getattr(obj_or_class, PYCKSON_MODEL)


def camel_case_name(python_name):
    return re.sub('_([a-z])', lambda match: match.group(1).upper(), python_name)


def get_enum_parser(obj_or_class) -> EnumParser:
    if not hasattr(obj_or_class, PYCKSON_ENUM_PARSER):
        return DefaultEnumParser(obj_or_class)
    return getattr(obj_or_class, PYCKSON_ENUM_PARSER)
