from datetime import datetime

import attr
import pytz


@attr.dataclass(frozen=True)
class DatetimeWithTz:
    """
    Сервис для получения даты с учетом часового пояса приложения
    """
    tz_info: pytz.timezone

    def now(self) -> datetime:
        now = datetime.now(tz=self.tz_info)
        return now
