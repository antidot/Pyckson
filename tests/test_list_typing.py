from dataclasses import dataclass

from pyckson import parse, serialize


def test_list_typing():
    @dataclass
    class Bar:
        y: int

    @dataclass
    class Foo:
        x: list[Bar]

    assert parse(Foo, {'x': [{'y': 2}, {'y': 3}]}) == Foo([Bar(2), Bar(3)])
    assert serialize(Foo([Bar(2), Bar(3)])) == {'x': [{'y': 2}, {'y': 3}]}


def test_set_typing():
    @dataclass(frozen=True)
    class Bar:
        y: int

    @dataclass
    class Foo:
        x: set[Bar]

    assert parse(Foo, {'x': [{'y': 2}, {'y': 3}]}) == Foo({Bar(2), Bar(3)})
    assert serialize(Foo({Bar(2), Bar(3)})) == {'x': [{'y': 2}, {'y': 3}]}
