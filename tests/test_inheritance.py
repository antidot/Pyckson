from dataclasses import dataclass
from typing import Optional

import pyckson
from pyckson import no_camel_case, serialize


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


def test_class_should_inherit_pyckson_parameters():
    @dataclass
    @no_camel_case
    class Parent:
        my_attribute: str

    @dataclass
    class Child(Parent):
        foo_bar: str

    assert serialize(Parent('foo')) == {'my_attribute': 'foo'}
    assert serialize(Child('foo', 'bar')) == {'my_attribute': 'foo', 'foo_bar': 'bar'}


def test_bug_18():
    @pyckson.rename(links="_links")
    @dataclass
    class Parent:
        links: str

    @dataclass
    class Child(Parent):
        pass

    json = '{"_links":"https://google.fr"}'

    obj = pyckson.loads(Parent, json)
    assert obj.links == 'https://google.fr'

    obj = pyckson.loads(Child, json)
    assert obj.links == 'https://google.fr'


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
