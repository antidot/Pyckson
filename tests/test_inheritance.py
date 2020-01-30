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
