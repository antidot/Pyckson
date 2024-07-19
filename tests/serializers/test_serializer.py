from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import List, Dict, Set, Optional, Union
from unittest import TestCase

from pyckson import dumps, explicit_nulls, enumvalues
from pyckson.dates.arrow import ArrowStringFormatter
from pyckson.decorators import pyckson, listtype, custom_serializer, settype, date_formatter
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

    def test_dumps_object_with_date(self):
        @date_formatter(ArrowStringFormatter())
        class Foo:
            def __init__(self, bar: date):
                self.bar = bar

        result = dumps(Foo(date(2018, 3, 8)))

        self.assertEqual(result, '{"bar": "2018-03-08"}')

    def test_class_with_optional_object_param_type(self):
        class Foo:
            def __init__(self, arg1: str):
                self.arg1 = arg1

        class Bar:
            def __init__(self, a_foo: Optional[Foo]):
                self.a_foo = a_foo

        result = serialize(Bar(Foo("foo")))

        self.assertEqual(result, {'aFoo': {'arg1': 'foo'}})

    def test_should_be_able_to_serialize_lists(self):
        class Foo:
            def __init__(self, a: int):
                self.a = a

        result = serialize([Foo(1), Foo(2)])

        self.assertEqual(result, [{'a': 1}, {'a': 2}])

    def test_should_be_able_to_serialize_typing_dicts(self):
        class Foo:
            def __init__(self, a: int):
                self.a = a

        class Bar:
            def __init__(self, b: Dict[str, Foo]):
                self.b = b

        result = serialize(Bar({'1': Foo(1), '2': Foo(2)}))

        self.assertEqual(result, {'b': {'1': {'a': 1}, '2': {'a': 2}}})

    def test_use_explicit_nulls(self):
        @pyckson
        @explicit_nulls
        class Foo:
            def __init__(self, a: str = None):
                self.a = a

        result = serialize(Foo(a=None))

        self.assertEqual(result, {'a': None})
        self.assertEqual(dumps(result), '{"a": null}')

    def test_should_be_able_to_serialize_union_type(self):
        class X:
            def __init__(self, x: str):
                self.x = x

        class Y:
            def __init__(self, y: str):
                self.y = y

        class Foo:
            def __init__(self, foo: Union[X, Y]):
                self.foo = foo

        assert serialize(Foo(X('a'))) == {'foo': {'x': 'a'}}


def test_serialize_union_str_values():
    class Foo:
        def __init__(self, e: Union[str, int]):
            self.e = e

    assert serialize(Foo('fooo')) == {'e': 'fooo'}


def test_serialize_union_int_values():
    class Foo:
        def __init__(self, e: Union[str, int]):
            self.e = e

    assert serialize(Foo(5)) == {'e': 5}


def test_serialize_union_list_values():
    class Foo:
        def __init__(self, e: Union[str, List[str]]):
            self.e = e

    assert serialize(Foo(['yo'])) == {'e': ['yo']}


def test_should_serialize_decimal():
    class Foo:
        def __init__(self, x: Decimal):
            self.x = x

    pi = '3.141592653589793238462643383279502884197'
    assert serialize(Foo(Decimal(pi))) == {'x': pi}


def test_serialize_int_enum_values():
    @enumvalues
    class MyEnum(Enum):
        FOO = 1
        BAR = 2

    class Foo:
        def __init__(self, e: MyEnum):
            self.e = e

    assert serialize(Foo(MyEnum.BAR)) == {'e': 2}


def test_serialize_str_enum_values():
    @enumvalues
    class MyEnum(Enum):
        FOO = 'fooo'
        BAR = 'baar'

    class Foo:
        def __init__(self, e: MyEnum):
            self.e = e

    assert serialize(Foo(MyEnum.BAR)) == {'e': 'baar'}
