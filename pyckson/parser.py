from enum import Enum
from typing import List

from pyckson.const import BASIC_TYPES, PYCKSON_TYPEINFO, PYCKSON_ENUM_OPTIONS, ENUM_CASE_INSENSITIVE
from pyckson.helpers import TypeProvider
from pyckson.helpers import get_model


def parse_class(cls, json):
    model = get_model(cls)
    obj_args = {}
    for attribute in model.attributes:
        if attribute.json_name in json:
            value = json[attribute.json_name]
            python_value = attribute.parser.parse(value)
            obj_args[attribute.python_name] = python_value
        elif not attribute.optional:
            raise ValueError('json is missing attribute {} to parse object {}'.format(attribute.json_name, cls))
    return cls(**obj_args)


def parse(cls, json):
    if cls in BASIC_TYPES:
        return BasicParser().parse(json)
    else:
        return parse_class(cls, json)


class Parser:
    def parse(self, json_value):
        pass


class BasicParser(Parser):
    def parse(self, json_value):
        return json_value


class ListParser(Parser):
    def __init__(self, sub_parser: Parser):
        self.sub_parser = sub_parser

    def parse(self, json_value):
        return [self.sub_parser.parse(item) for item in json_value]


class UnresolvedParser(Parser):
    def __init__(self, type_provider: TypeProvider):
        self.type_provider = type_provider

    def parse(self, json_value):
        obj_type = self.type_provider.get()
        return parse(obj_type, json_value)


class ClassParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, json_value):
        return parse_class(self.cls, json_value)


class DefaultEnumParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, value):
        return self.cls[value]


class CaseInsensitiveEnumParser(Parser):
    def __init__(self, cls):
        self.values = {member.name.lower(): member for member in cls}

    def parse(self, value):
        return self.values[value.lower()]


def get_parser(obj_type, parent_class, name_in_parent) -> Parser:
    if obj_type in BASIC_TYPES:
        return BasicParser()
    if type(obj_type) is str:
        return UnresolvedParser(TypeProvider(parent_class, obj_type))
    if obj_type is list:
        type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
        if name_in_parent in type_info:
            sub_type = type_info[name_in_parent]
            return ListParser(get_parser(sub_type, parent_class, name_in_parent))
        else:
            raise TypeError('list parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                  parent_class.__name__))
    if issubclass(obj_type, List):
        return ListParser(get_parser(obj_type.__args__[0], parent_class, name_in_parent))
    if issubclass(obj_type, Enum):
        options = getattr(obj_type, PYCKSON_ENUM_OPTIONS, {})
        if options.get(ENUM_CASE_INSENSITIVE, False):
            return CaseInsensitiveEnumParser(obj_type)
        else:
            return DefaultEnumParser(obj_type)
    return ClassParser(obj_type)
