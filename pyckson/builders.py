import sys
from inspect import Parameter, getmembers, signature

from pyckson.const import PYCKSON_TYPEINFO
from pyckson.helpers import get_name_rule
from pyckson.model import ListType, PycksonAttribute, PycksonModel, PycksonUnresolvedAttribute, UnresolvedListType


def type_provider(cls, name):
    def resolver():
        try:
            return getattr(sys.modules[cls.__module__], name)
        except AttributeError:
            raise TypeError('could not resolve string annotation {} in class {}'.format(name, cls.__name__))

    return resolver


class PycksonModelBuilder:
    def __init__(self, cls):
        self.cls = cls
        self.type_info = getattr(cls, PYCKSON_TYPEINFO, dict())
        self.name_rule = get_name_rule(cls)

    def find_constructor(self):
        for member in getmembers(self.cls):
            if member[0] == '__init__':
                return member[1]
        else:
            raise ValueError('no constructor_found')

    def build_model(self) -> PycksonModel:
        constructor = self.find_constructor()
        attributes = []
        for name, parameter in signature(constructor).parameters.items():
            if name != 'self':
                attribute = self.build_attribute(parameter)
                attributes.append(attribute)
        return PycksonModel(attributes)

    def build_attribute(self, parameter: Parameter) -> PycksonAttribute:
        json_name = self.name_rule(parameter.name)
        optional = parameter.default is not Parameter.empty
        if parameter.annotation is Parameter.empty:
            raise TypeError('parameter {} in class {} has no type'.format(parameter.name, self.cls.__name__))
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError('pyckson only handle named parameters')
        if parameter.annotation is list:
            if parameter.name in self.type_info:
                sub_type = self.type_info[parameter.name]
                attr_type = ListType(sub_type)
                if type(sub_type) is str:
                    attr_type = UnresolvedListType(type_provider(self.cls, sub_type))
                return PycksonAttribute(parameter.name, json_name, attr_type, optional)
            else:
                raise TypeError('list parameter {} in class {} has no subType'.format(parameter.name,
                                                                                      self.cls.__name__))
        if type(parameter.annotation) is str:
            return PycksonUnresolvedAttribute(parameter.name, json_name,
                                              type_provider(self.cls, parameter.annotation),
                                              optional)
        return PycksonAttribute(parameter.name, json_name, parameter.annotation, optional)
