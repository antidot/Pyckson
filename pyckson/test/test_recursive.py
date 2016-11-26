from unittest import TestCase

from pyckson import parse
from pyckson import pyckson, serialize
from pyckson.builders import PycksonModelBuilder


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
            parse(Fail('toto'))
