from functools import partial
import json

from pyckson.serializer import serialize
from pyckson.parser import parse


def dump(obj, fp, **kwargs):
    kwargs['default'] = serialize
    return json.dump(obj, fp, **kwargs)


def dumps(obj, **kwargs):
    kwargs['default'] = serialize
    return json.dumps(obj, **kwargs)


def load(obj_type, fp, **kwargs):
    kwargs['object_hook'] = partial(parse, obj_type=obj_type)
    return json.load(fp, **kwargs)


def loads(obj_type, s, **kwargs):
    kwargs['object_hook'] = partial(parse, obj_type=obj_type)
    return json.loads(s, **kwargs)
