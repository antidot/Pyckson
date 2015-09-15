from inspect import getmembers
import re
from pyckson.const import PYCKSON_ATTR, PYCKSON_MODEL


def is_pyckson(obj):
    return getattr(obj.__class__, PYCKSON_ATTR, False)


def get_model(obj):
    if not is_pyckson(obj):
        raise ValueError('{} has no pyckson info'.format(obj.__class__))
    return getattr(obj.__class__, PYCKSON_MODEL)


def find_class_constructor(cls):
    for member in getmembers(cls):
        if member[0] == '__init__':
            return member[1]
    else:
        raise ValueError('no constructor_found')


def camel_case_name(python_name):
    return re.sub('_([a-z])', lambda match: match.group(1).upper(), python_name)
