from datetime import datetime
from typing import List, Dict
from unittest import TestCase

from pyckson.decorators import pyckson, listtype
from pyckson.serializer import serialize


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

    def test_class_with_generic_list(self):
        @pyckson
        class Foo:
            def __init__(self, bar: List[str]):
                self.bar = bar

        result = serialize(Foo(['a', 'b']))
        self.assertEqual(result, {'bar': ['a', 'b']})

    def test_class_with_generic_object_list(self):
        @pyckson
        class Bar:
            def __init__(self, x: str):
                self.x = x

        @pyckson
        class Foo:
            def __init__(self, bar: List[Bar]):
                self.bar = bar

        result = serialize(Foo([Bar('a'), Bar('b')]))

        self.assertEqual(result, {'bar': [{'x': 'a'}, {'x': 'b'}]})

    def test_class_with_optional_attribute(self):
        @pyckson
        class Foo:
            def __init__(self, a: int, b: str = None):
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

    def test_with_unicode(self):
        class FakeString(str):
            pass

        @pyckson
        class Foo:
            def __init__(self, x: str):
                self.x = x

        result = serialize(Foo(FakeString('foo')))

        self.assertEqual(result, {'x': 'foo'})

    def test_with_date(self):
        @pyckson
        class Foo:
            def __init__(self, x: datetime):
                self.x = x

        date = datetime(2016, 2, 18, 10, 59, 0)
        result = serialize(Foo(date))

        self.assertEqual(result, {'x': date})

    def test_with_bytes(self):
        @pyckson
        class Foo:
            def __init__(self, x: bytes):
                self.x = x

        data = b"bar"
        result = serialize(Foo(data))

        self.assertEqual(result, {'x': data})

    def test_without_annotation(self):
        class Foo:
            def __init__(self, bar: List[str]):
                self.bar = bar

        result = serialize(Foo(['a', 'b']))

        self.assertEqual(result, {'bar': ['a', 'b']})

    def test_serialize_dict(self):
        class Foo:
            def __init__(self, foo: Dict[str, int]):
                self.foo = foo

        result = serialize(Foo({'a': 1, 'b': 2}))

        self.assertEqual(result, {'foo': {'a': 1, 'b': 2}})

    def test_serialize_old_dict(self):
        class Foo:
            def __init__(self, foo: dict):
                self.foo = foo

        result = serialize(Foo({'a': 1, 'b': 2}))

        self.assertEqual(result, {'foo': {'a': 1, 'b': 2}})
