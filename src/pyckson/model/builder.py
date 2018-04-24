from inspect import Parameter, getmembers, signature

from pyckson.const import PYCKSON_TYPEINFO
from pyckson.helpers import get_name_rule
from pyckson.model.model import PycksonModel, PycksonAttribute
from pyckson.model.union import inspect_optional_typing
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

    def build_attribute(self, parameter: Parameter) -> PycksonAttribute:
        python_name = parameter.name
        json_name = self.name_rule(parameter.name)
        optional = parameter.default is not Parameter.empty
        if parameter.annotation is Parameter.empty:
            raise TypeError('parameter {} in class {} has no type'.format(parameter.name, self.cls.__name__))
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError('pyckson only handle named parameters')
        is_optional, optional_type = inspect_optional_typing(parameter.annotation)
        if is_optional:
            return PycksonAttribute(python_name, json_name, optional_type, True,
                                    self.serializer_provider.get(optional_type, self.cls, python_name),
                                    self.parser_provider.get(optional_type, self.cls, python_name),
                                    force_default=parameter.default == Parameter.empty)

        return PycksonAttribute(python_name, json_name, parameter.annotation, optional,
                                self.serializer_provider.get(parameter.annotation, self.cls, python_name),
                                self.parser_provider.get(parameter.annotation, self.cls, python_name))
