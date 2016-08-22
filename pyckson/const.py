import datetime

from pyckson.model import ListType, UnresolvedListType

PYCKSON_ATTR = '__pyckson'
PYCKSON_TYPEINFO = '__pyckson_typeinfo'
PYCKSON_MODEL = '__pyckson_model'
PYCKSON_ENUM_PARSER = '__pyckson_enum'
PYCKSON_NAMERULE = '__pyckson_namerule'
BASIC_TYPES = [int, str, float, bool, datetime.date, datetime.time, datetime.datetime, bytes]
LIST_TYPES = [ListType, UnresolvedListType]
