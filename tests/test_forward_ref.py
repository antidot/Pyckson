from pyckson import Serializer, serialize, custom_serializer, Parser, parse
from pyckson.decorators import custom_parser


@custom_serializer('FooSerializer')
@custom_parser('FooParser')
class Foo:
    def __init__(self, bar):
        self.bar = bar


class FooSerializer(Serializer):
    def serialize(self, obj: Foo) -> dict:
        return {'toto': obj.bar}


class FooParser(Parser):
    def parse(self, json_value) -> Foo:
        return Foo(json_value['x'])


@custom_serializer('BarSerializer')
@custom_parser('BarParser')
class Bar:
    def __init__(self, x):
        self.x = x


class BarSerializer(Serializer):
    def serialize(self, obj: Bar):
        return 42


class BarParser(Parser):
    def parse(self, json_value) -> Bar:
        return Bar(42)


class Foo2:
    def __init__(self, bar: Bar):
        self.bar = bar


def test_custom_serializer_forwardref():
    result = serialize(Foo(42))

    assert result == {'toto': 42}


def test_custom_serializer_on_param_forwardref():
    result = serialize(Foo2(Bar(12)))

    assert result == {'bar': 42}


def test_custom_parser_forwardref():
    result = parse(Foo, {'x': 42})

    assert result.bar == 42


def test_custom_parser_on_param_forwardref():
    result = parse(Foo2, {'bar': {}})

    assert result.bar.x == 42
