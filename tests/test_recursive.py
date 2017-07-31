from typing import List
from unittest import TestCase

from pyckson import parse, serialize
from pyckson import pyckson


@pyckson
class Foo:
    def __init__(self, x: str, foo: 'Foo' = None):
        self.x = x
        self.foo = foo


@pyckson
class Bar:
    def __init__(self, quz: 'Quz' = None):
        self.quz = quz


@pyckson
class Quz:
    def __init__(self, x: str, bar: Bar = None):
        self.x = x
        self.bar = bar


@pyckson
class Fail:
    def __init__(self, bar: 'Toto'):
        self.bar = bar


class ClsWithForwardList:
    def __init__(self, x: List['ForwardListType']):
        self.x = x


class ForwardListType:
    def __init__(self, y: int):
        self.y = y


class TestForwardDeclarations(TestCase):
    def test_should_parse_recursive(self):
        result = parse(Foo, {'x': 'a', 'foo': {'x': 'b', 'foo': {'x': 'c'}}})
        self.assertEqual(result.x, 'a')
        self.assertEqual(result.foo.x, 'b')
        self.assertEqual(result.foo.foo.x, 'c')
        self.assertIsNone(result.foo.foo.foo)

    def test_should_parse_indirect_recursive(self):
        result = parse(Bar, {'quz': {'x': 'a', 'bar': {'quz': {'x': 'b'}}}})
        self.assertEqual(result.quz.x, 'a')
        self.assertEqual(result.quz.bar.quz.x, 'b')
        self.assertIsNone(result.quz.bar.quz.bar)

    def test_should_raise_error_on_unresolvedtype(self):
        with self.assertRaises(TypeError):
            parse(Fail, {'bar': 1})

    def test_should_parse_class_with_forwarf_list(self):
        result = parse(ClsWithForwardList, {'x': [{'y': 1}, {'y': 2}]})
        self.assertEqual(result.x[0].y, 1)
        self.assertEqual(result.x[1].y, 2)

    def test_should_serialize_class_with_forwarf_list(self):
        result = serialize(ClsWithForwardList([ForwardListType(1), ForwardListType(2)]))

        self.assertEqual(result, {'x': [{'y': 1}, {'y': 2}]})
