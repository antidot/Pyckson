from datetime import datetime, date

from pytest import fixture

from pyckson import date_formatter, parse, serialize
from pyckson.dates.helpers import get_class_date_formatter, configure_date_formatter
from pyckson.dates.model import DateFormatter
from pyckson.dates.raw_formatter import RawDateFormatter


class TestFormatter(DateFormatter):

    def parse_datetime(self, value) -> datetime:
        return datetime(2018, 3, 8, 14, 5, 10)

    def serialize_datetime(self, value: datetime):
        return 42

    def parse_date(self, value) -> date:
        return date(2018, 3, 8)

    def serialize_date(self, value: date):
        return 43


@fixture
def custom_date_serializer():
    configure_date_formatter(TestFormatter())
    yield
    configure_date_formatter(RawDateFormatter())


def test_should_use_class_formatter_if_present():
    @date_formatter(TestFormatter())
    class Foo:
        def __init__(self, bar: datetime):
            self.bar = bar

    assert type(get_class_date_formatter(Foo)) is TestFormatter


def test_should_use_global_formatter_otherwise(custom_date_serializer):
    class Foo:
        def __init__(self, bar: datetime):
            self.bar = bar

    assert type(get_class_date_formatter(Foo)) is TestFormatter


def test_parse_date_with_formatter():
    @date_formatter(TestFormatter())
    class Foo:
        def __init__(self, bar: datetime):
            self.bar = bar

    result = parse(Foo, {'bar': 42})

    assert result.bar == datetime(2018, 3, 8, 14, 5, 10)


def test_serialize_date_with_formatter():
    @date_formatter(TestFormatter())
    class Foo:
        def __init__(self, bar: date):
            self.bar = bar

    result = serialize(Foo(date(2018, 3, 8)))

    assert result == {'bar': 43}
