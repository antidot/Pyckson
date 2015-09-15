from inspect import getmembers, signature, Parameter, Signature
import re


PYCKSON_ATTR = '__pyckson'
PYCKSON_TYPEINFO = '__pyckson_typeinfo'
PYCKSON_MODEL = '__pyckson_model'


class ListType:
    def __init__(self, sub_type: type):
        self.sub_type = sub_type

    def __repr__(self):
        return '<class \'list[{}]\'>'.format(self.sub_type.__name__)


class PycksonInspector:
    @staticmethod
    def find_class_constructor(cls):
        for member in getmembers(cls):
            if member[0] == '__init__':
                return member[1]
        else:
            raise ValueError('no constructor_found')


class PycksonAttribute:
    def __init__(self, python_name, json_name, attr_type, optional=False):
        self.python_name = python_name
        self.json_name = json_name
        self.attr_type = attr_type
        self.optional = optional

    def __repr__(self):
        return 'PycksonAttribute({}, {}, {}, {})'.format(self.python_name,
                                                         self.json_name,
                                                         self.attr_type,
                                                         self.optional)

    @classmethod
    def from_parameter(cls, parameter: Parameter, sub_type: type=None):
        json_name = cls.camel_case_name(parameter.name)
        optional = parameter.default is None
        if parameter.annotation is Parameter.empty:
            raise TypeError('parameter {} has no type'.format(parameter.name))
        if parameter.annotation is list:
            if sub_type is None:
                raise TypeError('list parameter {} has no subType'.format(parameter.name))
            return cls(parameter.name, json_name, ListType(sub_type), optional)
        return cls(parameter.name, json_name, parameter.annotation, optional)

    @classmethod
    def camel_case_name(cls, python_name):
        return re.sub('_([a-z])', lambda match: match.group(1).upper(), python_name)


class PycksonModel:
    def __init__(self, attributes):
        self.attributes = attributes

    def __repr__(self):
        return repr(self.attributes)

    @classmethod
    def from_signature(cls, method_signature: Signature, type_info):
        attributes = []
        for name, parameter in method_signature.parameters.items():
            if name == 'self':
                continue
            if name in type_info:
                attribute = PycksonAttribute.from_parameter(parameter, type_info[name])
            else:
                attribute = PycksonAttribute.from_parameter(parameter)
            attributes.append(attribute)
        return cls(attributes)


def listtype(param_name, param_sub_type):
    def class_decorator(cls):
        type_info = getattr(cls, PYCKSON_TYPEINFO, dict())
        type_info[param_name] = param_sub_type
        setattr(cls, PYCKSON_TYPEINFO, type_info)
        return cls

    return class_decorator


def pyckson(cls):
    setattr(cls, PYCKSON_ATTR, True)
    constructor = PycksonInspector.find_class_constructor(cls)
    type_info = getattr(cls, PYCKSON_TYPEINFO, dict())
    model = PycksonModel.from_signature(signature(constructor), type_info)
    setattr(cls, PYCKSON_MODEL, model)
    return cls


def __is_pyckson(obj):
    return getattr(obj.__class__, PYCKSON_ATTR, False)


def __get_model(obj):
    if not __is_pyckson(obj):
        raise ValueError('{} has no pyckson info'.format(obj.__class__))
    return getattr(obj.__class__, PYCKSON_MODEL)


BASIC_TYPES = [int, str, float]


def serialize(obj):
    model = __get_model(obj)
    result = {}
    for attribute in model.attributes:
        value = getattr(obj, attribute.python_name, None)
        if value is None and attribute.optional:
            continue
        elif value is None:
            raise ValueError('attribute {} of {} is None but not marked as optional'.format(attribute.python_name, obj))

        if attribute.attr_type in BASIC_TYPES:
            result[attribute.json_name] = value
        elif type(attribute.attr_type) is ListType:
            if attribute.attr_type.sub_type in BASIC_TYPES:
                list_result = value
            else:
                list_result = [serialize(sub_value) for sub_value in value]
            result[attribute.json_name] = list_result
        else:
            result[attribute.json_name] = serialize(value)
    return result
