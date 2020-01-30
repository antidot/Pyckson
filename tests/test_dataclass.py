from dataclasses import dataclass

from pyckson import parse


def test_basic_dataclass():
    @dataclass
    class Foo:
        x: int
        y: int = 1

    assert parse(Foo, {'x': 2}) == Foo(2, 1)
