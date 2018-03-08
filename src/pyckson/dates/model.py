from datetime import datetime, date


class DateFormatter:
    def parse_datetime(self, value) -> datetime:
        pass

    def serialize_datetime(self, value: datetime):
        pass

    def parse_date(self, value) -> date:
        pass

    def serialize_date(self, value: date):
        pass
