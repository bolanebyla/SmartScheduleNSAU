from datetime import timedelta

import attr

from ..enums import WeekParities
from .datetime_with_tz import DatetimeWithTz


@attr.dataclass(frozen=True)
class WeekParityDeterminant:
    """
    Сервис определения четности недели
    """
    datetime_with_tz: DatetimeWithTz

    @staticmethod
    def _determine_parity_by_week_number(week_number: int) -> WeekParities:
        """
        Определяет четность недели по её номеру
        """
        if week_number % 2 == 0:
            week_parity = WeekParities.EVEN
        else:
            week_parity = WeekParities.ODD
        return week_parity

    def _get_current_week_number(self) -> int:
        """
        Получает номер текущей недели
        """
        week_number = self.datetime_with_tz.now().isocalendar().week
        return week_number

    def _get_next_week_number(self) -> int:
        """
        Получает номер следующей недели
        """
        week_number = (self.datetime_with_tz.now()
                       + timedelta(days=7)).isocalendar().week
        return week_number

    def get_current_week_parity(self) -> WeekParities:
        """
        Получает четность текущей недели
        """
        week_number = self._get_current_week_number()
        week_parity = self._determine_parity_by_week_number(
            week_number=week_number,
        )
        return week_parity

    def get_next_week_parity(self) -> WeekParities:
        """
        Получает четность следующей недели
        """
        week_number = self._get_next_week_number()
        week_parity = self._determine_parity_by_week_number(
            week_number=week_number,
        )
        return week_parity
