from pyckson.helpers import TypeProvider, is_base_type
from pyckson.parsers.base import Parser, BasicParser
from pyckson.providers import ModelProvider


class GenericParser(Parser):
    def __init__(self, cls, model_provider: ModelProvider):
        self.cls = cls
        self.model_provider = model_provider

    def parse(self, json_value):
        if is_base_type(self.cls):
            return BasicParser().parse(json_value)
        else:
            return ClassParser(self.cls, self.model_provider).parse(json_value)


class UnresolvedParser(Parser):
    def __init__(self, type_provider: TypeProvider, model_provider: ModelProvider):
        self.type_provider = type_provider
        self.model_provider = model_provider

    def parse(self, json_value):
        obj_type = self.type_provider.get()
        return GenericParser(obj_type, self.model_provider).parse(json_value)


class ClassParser(Parser):
    def __init__(self, cls, model_provider: ModelProvider):
        self.cls = cls
        self.model_provider = model_provider

    def parse(self, json_value):
        model = self.model_provider.get_or_build(self.cls)
        obj_args = {}
        for attribute in model.attributes:
            if attribute.json_name in json_value:
                value = json_value[attribute.json_name]
                python_value = attribute.parser.parse(value)
                obj_args[attribute.python_name] = python_value
            elif not attribute.optional:
                raise ValueError(
                    'json is missing attribute {} to parse object {}'.format(attribute.json_name, self.cls))
        return self.cls(**obj_args)
