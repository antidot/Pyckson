from datetime import datetime
from enum import Enum
from typing import Optional

import pytest

from pyckson import serialize, no_camel_case, explicit_nulls, use_camel_case, date_formatter, enumvalues, parse
from pyckson.dates.arrow import ArrowStringFormatter
from pyckson.defaults import reset_defaults, set_defaults


@pytest.fixture
def defaults():
    yield
    reset_defaults()


def test_should_apply_no_camel_case_to_all(defaults):
    class Foo:
        def __init__(self, some_thing: str):
            self.some_thing = some_thing

    set_defaults(no_camel_case)

    assert serialize(Foo('bar')) == {'some_thing': 'bar'}


def test_should_apply_multiple_defaults(defaults):
    class Foo:
        def __init__(self, some_thing: str, other_thing: Optional[str]):
            self.some_thing = some_thing
            self.other_thing = other_thing

    set_defaults(no_camel_case, explicit_nulls)

    assert serialize(Foo('bar', None)) == {'some_thing': 'bar', 'other_thing': None}


def test_annotation_should_override_defaults(defaults):
    @use_camel_case
    class Foo:
        def __init__(self, some_thing: str):
            self.some_thing = some_thing

    set_defaults(no_camel_case)

    assert serialize(Foo('bar')) == {'someThing': 'bar'}


def test_cannot_use_averything_at_a_default():
    with pytest.raises(ValueError):
        set_defaults(test_annotation_should_override_defaults)


def test_date_default(defaults):
    class Foo:
        def __init__(self, day: datetime):
            self.day = day

    set_defaults(date_formatter(ArrowStringFormatter()))

    assert serialize(Foo(datetime(2013, 5, 5, 12, 30, 45))) == {'day': '2013-05-05T12:30:45+00:00'}


def test_enum_values_default(defaults):
    class MyEnum(Enum):
        FOO = 1
        BAR = 2

    class Foo:
        def __init__(self, e: MyEnum):
            self.e = e

    set_defaults(enumvalues)

    assert serialize(Foo(MyEnum.FOO)) == {'e': 1}
    assert parse(Foo, {'e': 2}).e == MyEnum.BAR
