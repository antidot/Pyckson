import json

from pyckson.serializer import serialize
from pyckson.parser import parse


def dump(obj, fp, **kwargs):
    kwargs['default'] = serialize
    return json.dump(obj, fp, **kwargs)


def dumps(obj, **kwargs):
    kwargs['default'] = serialize
    return json.dumps(obj, **kwargs)


def load(cls, fp, **kwargs):
    def hook(obj):
        return parse(cls, obj)

    kwargs['object_hook'] = hook
    return json.load(fp, **kwargs)


def loads(cls, s, **kwargs):
    def hook(obj):
        return parse(cls, obj)

    kwargs['object_hook'] = hook
    return json.loads(s, **kwargs)
