from inspect import Parameter, getmembers, signature
from typing import Union

from pyckson.const import PYCKSON_TYPEINFO
from pyckson.helpers import get_name_rule
from pyckson.model.model import PycksonModel, PycksonAttribute
from pyckson.providers import SerializerProvider, ParserProvider


class PycksonModelBuilder:
    def __init__(self, cls, serializer_provider: SerializerProvider, parser_provider: ParserProvider):
        self.cls = cls
        self.serializer_provider = serializer_provider
        self.parser_provider = parser_provider
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

    def is_optional_type(self, param_type):
        # seems like at some point internal behavior on typing Union changed
        # https://bugs.launchpad.net/ubuntu/+source/python3.5/+bug/1650202
        if "Union" not in str(param_type):
            return False
        if hasattr(param_type, '__origin__'):
            is_union = param_type.__origin__ == Union
        else:
            is_union = issubclass(param_type, Union)

        if not is_union:
            return False

        union_args = self.get_union_params(param_type)
        return is_union and len(union_args) == 2 and isinstance(None, union_args[1])

    def get_union_params(self, param_type):
        if hasattr(param_type, '__args__'):
            return param_type.__args__
        else:
            return param_type.__union_params__

    def build_attribute(self, parameter: Parameter) -> PycksonAttribute:
        python_name = parameter.name
        json_name = self.name_rule(parameter.name)
        optional = parameter.default is not Parameter.empty
        if parameter.annotation is Parameter.empty:
            raise TypeError('parameter {} in class {} has no type'.format(parameter.name, self.cls.__name__))
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError('pyckson only handle named parameters')
        if self.is_optional_type(parameter.annotation):
            return PycksonAttribute(python_name, json_name, self.get_union_params(parameter.annotation)[0], True,
                                    self.serializer_provider.get(str, self.cls, python_name),
                                    self.parser_provider.get(str, self.cls, python_name))

        return PycksonAttribute(python_name, json_name, parameter.annotation, optional,
                                self.serializer_provider.get(parameter.annotation, self.cls, python_name),
                                self.parser_provider.get(parameter.annotation, self.cls, python_name))
