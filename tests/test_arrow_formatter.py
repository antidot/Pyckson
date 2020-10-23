import os
from datetime import datetime, date

from pyckson.dates.arrow import ArrowStringFormatter, ArrowTimestampFormatter


def test_parse_string_datetimes():
    formatter = ArrowStringFormatter()

    assert formatter.parse_datetime('2013-05-05 12:30:45') == datetime(2013, 5, 5, 12, 30, 45)
    assert formatter.parse_date('2013-05-05 12:30:45') == date(2013, 5, 5)


def test_serialize_string_datetimes():
    formatter = ArrowStringFormatter()

    assert formatter.serialize_datetime(datetime(2013, 5, 5, 12, 30, 45)) == '2013-05-05T12:30:45+00:00'
    assert formatter.serialize_date(date(2013, 5, 5)) == '2013-05-05'


def test_parse_int_datetimes():
    formatter = ArrowTimestampFormatter()

    assert formatter.parse_datetime(1367757045) == datetime(2013, 5, 5, 12, 30, 45)
    if os.name != "nt":
        assert formatter.parse_date(-11665296000) == date(1600, 5, 5)


def test_serialize_int_datetimes():
    formatter = ArrowTimestampFormatter()

    assert formatter.serialize_datetime(datetime(2013, 5, 5, 12, 30, 45)) == 1367757045
    assert formatter.serialize_date(date(1600, 5, 5)) == -11665296000
