from unittest import TestCase

from pyckson.serializer import serialize
from pyckson.decorators import pyckson, listtype


class SerializerTest(TestCase):
    def test_simple_class(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        result = serialize(Foo('bar'))

        self.assertEqual(result, {'bar': 'bar'})

    def test_class_with_list(self):
        @pyckson
        @listtype('bar', str)
        class Foo:
            def __init__(self, bar: list):
                self.bar = bar

        result = serialize(Foo(['a', 'b']))

        self.assertEqual(result, {'bar': ['a', 'b']})

    def test_class_with_optional_attribute(self):
        @pyckson
        class Foo:
            def __init__(self, a: int, b:str=None):
                self.a = a
                self.b = b

        result = serialize(Foo(42))

        self.assertEqual(result, {'a': 42})

    def test_class_with_missing_attribute(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        with self.assertRaises(ValueError):
            serialize(Foo(None))

    def test_should_serialize_empty_mandatory_list(self):
        @pyckson
        @listtype('bar', str)
        class Foo:
            def __init__(self, bar: list):
                self.bar = bar

        result = serialize(Foo([]))

        self.assertEqual(result, {'bar': []})

    def test_should_serialize_list_with_unresolved_type(self):
        @pyckson
        class Bar:
            def __init__(self, x: str):
                self.x = x

        @pyckson
        @listtype('bar', Bar)
        class Foo:
            def __init__(self, bar: list):
                self.bar = bar

        result = serialize(Foo([Bar('y')]))

        self.assertEqual(result, {'bar': [{'x': 'y'}]})
