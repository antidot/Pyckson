from datetime import datetime
from enum import Enum
from typing import List
from unittest import TestCase

from pyckson.decorators import pyckson, listtype, caseinsensitive
from pyckson.parser import parse


class ParserTest(TestCase):
    def test_simple_class(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        result = parse(Foo, {'bar': 'bar'})

        self.assertEqual(result.bar, 'bar')

    def test_class_with_list(self):
        @pyckson
        @listtype('bar', str)
        class Foo:
            def __init__(self, bar: list):
                self.bar = bar

        result = parse(Foo, {'bar': ['a', 'b']})

        self.assertListEqual(result.bar, ['a', 'b'])

    def test_class_with_generic_list(self):
        @pyckson
        class Foo:
            def __init__(self, bar: List[str]):
                self.bar = bar

        result = parse(Foo, {'bar': ['a', 'b']})
        self.assertListEqual(result.bar, ['a', 'b'])

    def test_class_with_generic_object_list(self):
        @pyckson
        class Bar:
            def __init__(self, x: str):
                self.x = x

            def __eq__(self, other):
                return self.x == other.x

        @pyckson
        class Foo:
            def __init__(self, bar: List[Bar]):
                self.bar = bar

        result = parse(Foo, {'bar': [{'x': 'a'}, {'x': 'b'}]})
        self.assertListEqual(result.bar, [Bar('a'), Bar('b')])

    def test_class_with_optional_attribute(self):
        @pyckson
        class Foo:
            def __init__(self, a: int, b: str = None):
                self.a = a
                self.b = b

        result = parse(Foo, {'a': 42})

        self.assertEqual(result.a, 42)
        self.assertIsNone(result.b)

    def test_class_with_missing_attribute(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        with self.assertRaises(ValueError):
            parse(Foo, {})

    def test_parse_with_insensitive_enum(self):
        @caseinsensitive
        class Foo(Enum):
            a = 1

        @pyckson
        class Bar:
            def __init__(self, foo: Foo):
                self.foo = foo

        result = parse(Bar, {'foo': 'A'})

        self.assertEqual(result.foo, Foo.a)

    def test_with_date(self):
        @pyckson
        class Foo:
            def __init__(self, x: datetime):
                self.x = x

        date = datetime(2016, 2, 18, 10, 59, 0)
        result = parse(Foo, {'x': date})

        self.assertEqual(result.x, date)

    def test_with_bytes(self):
        @pyckson
        class Foo:
            def __init__(self, x: bytes):
                self.x = x

        data = b"bar"
        result = parse(Foo, {'x': data})

        self.assertEqual(result.x, data)

    def test_without_annotation(self):
        class Foo:
            def __init__(self, bar: List[str]):
                self.bar = bar

        result = parse(Foo, {'bar': ['a', 'b']})

        self.assertListEqual(result.bar, ['a', 'b'])
