from inspect import Parameter, getmembers, signature
import sys

from pyckson.const import PYCKSON_TYPEINFO
from pyckson.model import ListType, PycksonAttribute, PycksonModel
from pyckson.helpers import camel_case_name


class PycksonModelBuilder:
    def __init__(self, cls):
        self.cls = cls
        self.type_info = getattr(cls, PYCKSON_TYPEINFO, dict())

    def find_constructor(self):
        for member in getmembers(self.cls):
            if member[0] == '__init__':
                return member[1]
        else:
            raise ValueError('no constructor_found')

    def get_class_from_name(self, name):
        try:
            return getattr(sys.modules[self.cls.__module__], name)
        except AttributeError:
            raise TypeError('could not resolve string annotation {} in class {}'.format(name, self.cls.__name__))

    def build_model(self) -> PycksonModel:
        constructor = self.find_constructor()
        attributes = []
        for name, parameter in signature(constructor).parameters.items():
            if name != 'self':
                attribute = self.build_attribute(parameter)
                attributes.append(attribute)
        return PycksonModel(attributes)

    def build_attribute(self, parameter: Parameter) -> PycksonAttribute:
        json_name = camel_case_name(parameter.name)
        optional = parameter.default is None
        if parameter.annotation is Parameter.empty:
            raise TypeError('parameter {} in class {} has no type'.format(parameter.name, self.cls.__name__))
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError('pyckson only handle named parameters')
        if parameter.annotation is list:
            if parameter.name in self.type_info:
                return PycksonAttribute(parameter.name, json_name, ListType(self.type_info[parameter.name]), optional)
            else:
                raise TypeError('list parameter {} in class {} has no subType'.format(parameter.name, self.cls.__name__))
        if type(parameter.annotation) is str:
            real_type = self.get_class_from_name(parameter.annotation)
            return PycksonAttribute(parameter.name, json_name, real_type, optional)
        return PycksonAttribute(parameter.name, json_name, parameter.annotation, optional)
