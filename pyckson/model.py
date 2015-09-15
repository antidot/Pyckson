from inspect import Parameter, Signature

from pyckson.helpers import camel_case_name


class ListType:
    def __init__(self, sub_type: type):
        self.sub_type = sub_type

    def __repr__(self):
        return '<class \'list[{}]\'>'.format(self.sub_type.__name__)


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
        json_name = camel_case_name(parameter.name)
        optional = parameter.default is None
        if parameter.annotation is Parameter.empty:
            raise TypeError('parameter {} has no type'.format(parameter.name))
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError('pyckson only handle named parameters')
        if parameter.annotation is list:
            if sub_type is None:
                raise TypeError('list parameter {} has no subType'.format(parameter.name))
            return cls(parameter.name, json_name, ListType(sub_type), optional)
        return cls(parameter.name, json_name, parameter.annotation, optional)


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
