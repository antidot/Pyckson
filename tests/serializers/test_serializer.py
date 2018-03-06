from datetime import datetime
from typing import List, Dict, Set, Optional
from unittest import TestCase

from pyckson.decorators import pyckson, listtype, custom_serializer, settype
from pyckson.serializer import serialize
from pyckson.serializers.base import Serializer


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

    def test_serialize_double_list(self):
        class Foo:
            def __init__(self, bar: List[List[str]]):
                self.bar = bar

        result = serialize(Foo([['a', 'b'], ['c']]))

        self.assertEqual(result, {'bar': [['a', 'b'], ['c']]})

    def test_custom_serializer(self):
        class Foo:
            def __init__(self, bar):
                self.bar = bar

        class FooSerializer(Serializer):
            def serialize(self, obj: Foo) -> dict:
                return {'toto': obj.bar}

        custom_serializer(FooSerializer)(Foo)

        result = serialize(Foo(42))

        self.assertEqual(result, {'toto': 42})

    def test_custom_serializer_on_param(self):
        class Bar:
            def __init__(self):
                pass

        class BarSerializer(Serializer):
            def serialize(self, obj: Bar):
                return 42

        class Foo:
            def __init__(self, bar: Bar):
                self.bar = bar

        custom_serializer(BarSerializer)(Bar)

        result = serialize(Foo(Bar()))

        self.assertEqual(result, {'bar': 42})

    def test_serialize_set_as_list(self):
        class Foo:
            def __init__(self, x: Set[int]):
                self.x = x

        result = serialize(Foo({1, 2}))

        # because of unknown ordering
        self.assertSetEqual(set(result['x']), {1, 2})

    def test_class_with_legacy_set(self):
        @pyckson
        @settype('bar', str)
        class Foo:
            def __init__(self, bar: set):
                self.bar = bar

        result = serialize(Foo({'a', 'b'}))

        # because of unknown ordering
        self.assertSetEqual(set(result['bar']), {'a', 'b'})

    def test_class_with_optional_param_type(self):
        class Foo:
            def __init__(self, bar: Optional[str]):
                self.bar = bar

        result = serialize(Foo('a'))

        self.assertEqual(result, {'bar': 'a'})

    def test_class_with_optional_param_type_absent(self):
        class Foo:
            def __init__(self, bar: Optional[str]):
                self.bar = bar

        result = serialize(Foo(None))

        self.assertEqual(result, {})
