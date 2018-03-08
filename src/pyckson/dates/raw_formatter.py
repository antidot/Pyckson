from datetime import datetime, date

from pyckson.dates.model import DateFormatter


class RawDateFormatter(DateFormatter):
    def parse_datetime(self, value) -> datetime:
        return value

    def serialize_datetime(self, value: datetime):
        return value

    def parse_date(self, value) -> date:
        return value

    def serialize_date(self, value: date):
        return value
