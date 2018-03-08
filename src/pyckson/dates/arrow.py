from datetime import datetime, date

import arrow

from pyckson.dates.model import DateFormatter


class ArrowStringFormatter(DateFormatter):
    def parse_datetime(self, value) -> datetime:
        return arrow.get(value).naive

    def serialize_datetime(self, value: datetime):
        return arrow.Arrow.fromdatetime(value).isoformat()

    def parse_date(self, value) -> date:
        return arrow.get(value).date()

    def serialize_date(self, value: date):
        return arrow.Arrow.fromdate(value).format(fmt='YYYY-MM-DD')


class ArrowTimestampFormatter(DateFormatter):
    def parse_datetime(self, value) -> datetime:
        return arrow.get(value).naive

    def serialize_datetime(self, value: datetime):
        return arrow.Arrow.fromdatetime(value).timestamp

    def parse_date(self, value) -> date:
        return arrow.get(value).date()

    def serialize_date(self, value: date):
        return arrow.Arrow.fromdate(value).timestamp
