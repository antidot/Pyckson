from pyckson.const import PYCKSON_DATE_FORMATTER
from pyckson.dates.model import DateFormatter
from pyckson.dates.raw_formatter import RawDateFormatter

global_date_formatter = RawDateFormatter()


def configure_date_formatter(formatter: DateFormatter):
    global global_date_formatter
    global_date_formatter = formatter


def get_date_formatter() -> DateFormatter:
    return global_date_formatter


def get_class_date_formatter(cls) -> DateFormatter:
    if hasattr(cls, PYCKSON_DATE_FORMATTER):
        return getattr(cls, PYCKSON_DATE_FORMATTER)
    else:
        return get_date_formatter()
