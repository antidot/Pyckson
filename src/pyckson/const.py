import datetime

PYCKSON_ATTR = '__pyckson'
PYCKSON_TYPEINFO = '__pyckson_typeinfo'
PYCKSON_MODEL = '__pyckson_model'
PYCKSON_ENUM_OPTIONS = '__pyckson_enum'
PYCKSON_NAMERULE = '__pyckson_namerule'
PYCKSON_SERIALIZER = '__pyckson_serializer'
PYCKSON_PARSER = '__pyckson_parser'
PYCKSON_DATE_FORMATTER = '__pyckson_date_formatter'
PYCKSON_EXPLICIT_NULLS = '__pyckson_explicit_nulls'
BASIC_TYPES = [int, str, float]
EXTRA_TYPES = [bool, bytes, datetime.time]
DATE_TYPES = [datetime.date, datetime.datetime]

ENUM_CASE_INSENSITIVE = 'case-insensitive'
