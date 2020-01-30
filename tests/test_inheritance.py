from dataclasses import dataclass
from typing import Optional

import pyckson


def test_bug_14():
    @dataclass
    class Parent:
        mandatory_one: str
        mandatory_two: str

    @dataclass
    class Child(Parent):
        mandatory_two: Optional[str]

    x = '{"mandatoryOne": "toto", "mandatoryTwo": "plip"}'
    y = '{"mandatoryOne": "toto"}'

    assert pyckson.loads(Parent, x) == Parent('toto', 'plip')
    assert pyckson.loads(Child, y) == Child('toto', None)


def test_mangled_attributes():
    @pyckson.pyckson
    @dataclass
    class Parent:
        mandatory_one: str
        mandatory_two: str

    @pyckson.pyckson
    @dataclass
    class Child(Parent):
        mandatory_two: Optional[str]

    assert getattr(Parent, '__Parent_pyckson') is True
    assert getattr(Child, '__Child_pyckson') is True
    assert not hasattr(Parent, '__Child_pyckson')
    assert hasattr(Child, '__Parent_pyckson')
