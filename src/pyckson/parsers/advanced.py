from datetime import date, datetime

from pyckson.const import PYCKSON_PARSER
from pyckson.dates.helpers import get_class_date_formatter
from pyckson.helpers import TypeProvider, is_base_type, get_custom_parser, is_base_type_with_cast
from pyckson.parsers.base import Parser, BasicParser, BasicParserWithCast
from pyckson.providers import ModelProvider


class GenericParser(Parser):
    def __init__(self, cls, model_provider: ModelProvider):
        self.cls = cls
        self.model_provider = model_provider

    def parse(self, json_value):
        if is_base_type(self.cls):
            return BasicParser().parse(json_value)
        elif is_base_type_with_cast(self.cls):
            return BasicParserWithCast(self.cls).parse(json_value)
        elif hasattr(self.cls, PYCKSON_PARSER):
            return get_custom_parser(self.cls).parse(json_value)
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
            if attribute.json_name in json_value and json_value[attribute.json_name] is not None:
                value = json_value[attribute.json_name]
                python_value = attribute.parser.parse(value)
                obj_args[attribute.python_name] = python_value
            elif attribute.optional and attribute.force_default:
                obj_args[attribute.python_name] = None
            elif not attribute.optional:
                raise ValueError(
                    'json is missing attribute {} to parse object {}'.format(attribute.json_name, self.cls))
        return self.cls(**obj_args)


class CustomDeferredParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, json_value):
        return get_custom_parser(self.cls).parse(json_value)


class DateParser(Parser):
    def __init__(self, cls, obj_type):
        self.cls = cls
        self.obj_type = obj_type

    def parse(self, json_value):
        formatter = get_class_date_formatter(self.cls)
        if self.obj_type is date:
            return formatter.parse_date(json_value)
        if self.obj_type is datetime:
            return formatter.parse_datetime(json_value)
