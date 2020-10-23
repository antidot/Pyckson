import datetime

PYCKSON_ATTR = '__{cls}_pyckson'
PYCKSON_TYPEINFO = '__pyckson_typeinfo'
PYCKSON_MODEL = '__{cls}_pyckson_model'
PYCKSON_ENUM_OPTIONS = '__pyckson_enum'
PYCKSON_NAMERULE = '__pyckson_namerule'
PYCKSON_SERIALIZER = '__pyckson_serializer'
PYCKSON_PARSER = '__pyckson_parser'
PYCKSON_DATE_FORMATTER = '__pyckson_date_formatter'
PYCKSON_EXPLICIT_NULLS = '__pyckson_explicit_nulls'
PYCKSON_RULE_ATTR = '__{cls}_pyckson_rule_attr'
BASIC_TYPES = [int, str, float]
EXTRA_TYPES = [bool, bytes, datetime.time]
DATE_TYPES = [datetime.date, datetime.datetime]

ENUM_CASE_INSENSITIVE = 'case-insensitive'
ENUM_USE_VALUES = 'use-values'


def get_cls_attr(cls, attr, default=None):
    return getattr(cls, attr.format(cls=cls.__name__), default)


def set_cls_attr(cls, attr, value):
    setattr(cls, attr.format(cls=cls.__name__), value)


def has_cls_attr(cls, attr):
    return hasattr(cls, '__name__') and hasattr(cls, attr.format(cls=cls.__name__))
