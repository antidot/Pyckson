from pyckson.builders import PycksonModelBuilder
from pyckson.const import PYCKSON_TYPEINFO, PYCKSON_ATTR, PYCKSON_MODEL


def listtype(param_name, param_sub_type):
    def class_decorator(cls):
        type_info = getattr(cls, PYCKSON_TYPEINFO, dict())
        type_info[param_name] = param_sub_type
        setattr(cls, PYCKSON_TYPEINFO, type_info)
        return cls

    return class_decorator


def pyckson(cls):
    setattr(cls, PYCKSON_ATTR, True)
    model = PycksonModelBuilder(cls).build_model()
    setattr(cls, PYCKSON_MODEL, model)
    return cls
