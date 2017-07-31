from enum import Enum
from unittest import TestCase

from pyckson.parsers.base import DefaultEnumParser, CaseInsensitiveEnumParser


class MyEnum(Enum):
    a = 1
    A = 2
    b = 3


class DefaultEnumParserTest(TestCase):
    def setUp(self):
        self.parser = DefaultEnumParser(MyEnum)

    def test_should_parse_value_in_enum(self):
        self.assertEqual(self.parser.parse('a'), MyEnum.a)
        self.assertEqual(self.parser.parse('A'), MyEnum.A)
        self.assertEqual(self.parser.parse('b'), MyEnum.b)

    def test_should_not_parse_uppercase_not_in_enum(self):
        with self.assertRaises(KeyError):
            self.parser.parse('B')

    def test_should_not_parse_value_not_in_enum(self):
        with self.assertRaises(KeyError):
            self.parser.parse('c')


class MyInsensitiveEnum(Enum):
    a = 1
    B = 2


class CaseInsensitiveEnumParserTest(TestCase):
    def setUp(self):
        self.parser = CaseInsensitiveEnumParser(MyInsensitiveEnum)

    def test_should_parse_value_in_enum(self):
        self.assertEqual(self.parser.parse('a'), MyInsensitiveEnum.a)
        self.assertEqual(self.parser.parse('B'), MyInsensitiveEnum.B)

    def test_should_parse_case_insensitive(self):
        self.assertEqual(self.parser.parse('A'), MyInsensitiveEnum.a)
        self.assertEqual(self.parser.parse('b'), MyInsensitiveEnum.B)

    def test_should_not_parse_value_not_in_enum(self):
        with self.assertRaises(KeyError):
            self.parser.parse('c')
