import re
import sys
from enum import Enum

from typing import List, Set, Dict, Union

try:
    from typing import _ForwardRef as ForwardRef
except ImportError:
    from typing import ForwardRef

from pyckson.const import PYCKSON_ATTR, BASIC_TYPES, PYCKSON_NAMERULE, PYCKSON_SERIALIZER, PYCKSON_PARSER, EXTRA_TYPES, \
    get_cls_attr, set_cls_attr, PYCKSON_RULE_ATTR
from pyckson.parsers.base import Parser
from pyckson.serializers.base import Serializer


def is_pyckson(obj_type):
    return get_cls_attr(obj_type, PYCKSON_ATTR, False)


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
    return get_cls_attr(obj_type, PYCKSON_NAMERULE, camel_case_name)


def is_base_type_with_cast(obj):
    for btype in BASIC_TYPES:
        if isinstance(obj, btype):
            return True
    return False


def is_base_type(obj):
    for btype in EXTRA_TYPES:
        if isinstance(obj, btype):
            return True
    return False


class TypeProvider:
    def __init__(self, cls, name):
        self.cls = cls
        self.name = name.__forward_arg__ if type(name) is ForwardRef else name

    def get(self):
        try:
            return getattr(sys.modules[self.cls.__module__], self.name)
        except AttributeError:
            raise TypeError('could not resolve string annotation {} in class {}'.format(self.name, self.cls.__name__))


def get_custom_serializer(cls) -> Serializer:
    serializer = get_cls_attr(cls, PYCKSON_SERIALIZER)
    if isinstance(serializer, str):
        serializer = TypeProvider(cls, serializer).get()
    return serializer()


def get_custom_parser(cls) -> Parser:
    parser = get_cls_attr(cls, PYCKSON_PARSER)
    if isinstance(parser, str):
        parser = TypeProvider(cls, parser).get()
    return parser()


def is_list_annotation(annotation):
    if hasattr(annotation, '_name'):
        return annotation._name == 'List'
    else:
        try:
            return issubclass(annotation, List) or annotation.__name__ == 'list'
        except TypeError:
            return False


def is_set_annotation(annotation):
    if hasattr(annotation, '_name'):
        return annotation._name == 'Set'
    else:
        try:
            return issubclass(annotation, Set) or annotation.__name__ == 'set'
        except TypeError:
            return False


def is_enum_annotation(annotation):
    if hasattr(annotation, '_name'):
        return annotation._name == 'Enum'
    else:
        try:
            return issubclass(annotation, Enum)
        except TypeError:
            return False


def is_basic_dict_annotation(annotation):
    if type(annotation) is type and issubclass(annotation, dict):
        return True
    return False


def is_typing_dict_annotation(annotation):
    if hasattr(annotation, '_name'):
        return annotation._name == 'Dict'
    else:
        try:
            return issubclass(annotation, Dict) or annotation.__name__ == 'dict'
        except TypeError:
            return False


def is_union_annotation(annotation) -> bool:
    if hasattr(annotation, '__origin__'):
        return annotation.__origin__ == Union
    return False


def using(attr):
    def class_decorator(cls):
        set_cls_attr(cls, PYCKSON_RULE_ATTR, attr)
        return cls

    return class_decorator
