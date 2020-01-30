import datetime

PYCKSON_ATTR = '__{cls}_pyckson'
PYCKSON_TYPEINFO = '__{cls}_pyckson_typeinfo'
PYCKSON_MODEL = '__{cls}_pyckson_model'
PYCKSON_ENUM_OPTIONS = '__{cls}_pyckson_enum'
PYCKSON_NAMERULE = '__{cls}_pyckson_namerule'
PYCKSON_SERIALIZER = '__{cls}_pyckson_serializer'
PYCKSON_PARSER = '__{cls}_pyckson_parser'
PYCKSON_DATE_FORMATTER = '__{cls}_pyckson_date_formatter'
PYCKSON_EXPLICIT_NULLS = '__{cls}_pyckson_explicit_nulls'
BASIC_TYPES = [int, str, float]
EXTRA_TYPES = [bool, bytes, datetime.time]
DATE_TYPES = [datetime.date, datetime.datetime]

ENUM_CASE_INSENSITIVE = 'case-insensitive'


def get_cls_attr(cls, attr, default=None):
    return getattr(cls, attr.format(cls=cls.__name__), default)


def set_cls_attr(cls, attr, value):
    setattr(cls, attr.format(cls=cls.__name__), value)


def has_cls_attr(cls, attr):
    return hasattr(cls, attr.format(cls=cls.__name__))
