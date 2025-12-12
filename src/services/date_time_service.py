from datetime import datetime, timedelta, time, timezone


class DateTimeService:
    @staticmethod
    def futur_date_and_time(days: int, hours: int):
        return datetime.combine(
            (datetime.now(timezone.utc) + timedelta(days=days)).date(),
            time(hours, 0, tzinfo=timezone.utc),
        )
