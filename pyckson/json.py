import json

from pyckson import serialize


def dump(obj, **kwargs):
    kwargs['default'] = serialize
    json.dump(obj, **kwargs)


def dumps(obj, fp, **kwargs):
    kwargs['default'] = serialize
    json.dumps(obj, fp, **kwargs)
