from enum import Enum

from pyckson.const import PYCKSON_TYPEINFO, PYCKSON_NAMERULE, PYCKSON_ENUM_OPTIONS, \
    ENUM_CASE_INSENSITIVE, PYCKSON_SERIALIZER, PYCKSON_PARSER, PYCKSON_DATE_FORMATTER, PYCKSON_EXPLICIT_NULLS, \
    get_cls_attr, set_cls_attr
from pyckson.dates.model import DateFormatter
from pyckson.helpers import same_name, name_by_dict, get_name_rule
from pyckson.model.helpers import ModelProviderImpl
from pyckson.parser import parse


def listtype(param_name, param_sub_type):
    def class_decorator(cls):
        type_info = get_cls_attr(cls, PYCKSON_TYPEINFO, dict())
        type_info[param_name] = param_sub_type
        set_cls_attr(cls, PYCKSON_TYPEINFO, type_info)
        return cls

    return class_decorator


settype = listtype


def pyckson(cls):
    ModelProviderImpl().get_or_build(cls)
    setattr(cls, 'parse', lambda json: parse(cls, json))
    return cls


def caseinsensitive(cls):
    """Annotation function to set an Enum to be case insensitive on parsing"""
    if not issubclass(cls, Enum):
        raise TypeError('caseinsensitive decorator can only be applied to subclasses of enum.Enum')
    enum_options = get_cls_attr(cls, PYCKSON_ENUM_OPTIONS, {})
    enum_options[ENUM_CASE_INSENSITIVE] = True
    set_cls_attr(cls, PYCKSON_ENUM_OPTIONS, enum_options)
    return cls


def namerule(name_function):
    def class_decorator(cls):
        set_cls_attr(cls, PYCKSON_NAMERULE, name_function)
        return cls

    return class_decorator


def no_camel_case(cls):
    set_cls_attr(cls, PYCKSON_NAMERULE, same_name)
    return cls


def rename(**kwargs):
    def class_decorator(cls):
        name_function = name_by_dict(kwargs, get_name_rule(cls))
        set_cls_attr(cls, PYCKSON_NAMERULE, name_function)
        return cls

    return class_decorator


def custom_serializer(serializer_cls):
    def class_decorator(cls):
        set_cls_attr(cls, PYCKSON_SERIALIZER, serializer_cls)
        return cls

    return class_decorator


def custom_parser(parser_cls):
    def class_decorator(cls):
        set_cls_attr(cls, PYCKSON_PARSER, parser_cls)
        return cls

    return class_decorator


def date_formatter(formatter: DateFormatter):
    def class_decorator(cls):
        set_cls_attr(cls, PYCKSON_DATE_FORMATTER, formatter)
        return cls

    return class_decorator


def explicit_nulls(cls):
    set_cls_attr(cls, PYCKSON_EXPLICIT_NULLS, True)
    return cls
