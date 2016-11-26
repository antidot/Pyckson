import json

from pyckson.serializer import serialize
from pyckson.parser import parse


def dump(obj, fp, **kwargs):
    """wrapper for :py:func:`json.dump`"""
    kwargs['default'] = serialize
    return json.dump(obj, fp, **kwargs)


def dumps(obj, **kwargs):
    """wrapper for :py:func:`json.dumps`"""
    kwargs['default'] = serialize
    return json.dumps(obj, **kwargs)


def load(cls, fp, **kwargs):
    """wrapper for :py:func:`json.load`"""
    json_obj = json.load(fp, **kwargs)
    return parse(cls, json_obj)


def loads(cls, s, **kwargs):
    """wrapper for :py:func:`json.loads`"""
    json_obj = json.loads(s, **kwargs)
    return parse(cls, json_obj)
