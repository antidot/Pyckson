from decimal import Decimal
from enum import Enum


class Parser:
    def parse(self, json_value):
        pass


class BasicParser(Parser):
    def parse(self, json_value):
        return json_value


class BasicParserWithCast(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, json_value):
        return self.cls(json_value)


class ListParser(Parser):
    def __init__(self, sub_parser: Parser):
        self.sub_parser = sub_parser
        self.cls = list

    def parse(self, json_value):
        return [self.sub_parser.parse(item) for item in json_value]


class SetParser(Parser):
    def __init__(self, sub_parser: Parser):
        self.sub_parser = sub_parser
        self.cls = set

    def parse(self, json_value):
        return {self.sub_parser.parse(item) for item in json_value}


class DefaultEnumParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, value):
        return self.cls[value]


class CaseInsensitiveEnumParser(Parser):
    def __init__(self, cls):
        self.values = {member.name.lower(): member for member in cls}
        self.cls = Enum

    def parse(self, value):
        return self.values[value.lower()]


class ValuesEnumParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, value):
        return self.cls(value)


class BasicDictParser(Parser):
    def parse(self, json_value):
        return json_value


class TypingDictParser(Parser):
    def __init__(self, value_parser: Parser):
        self.value_parser = value_parser

    def parse(self, json_value):
        return {k: self.value_parser.parse(v) for k, v in json_value.items()}


class DecimalParser(Parser):
    def parse(self, json_value):
        return Decimal(json_value)
