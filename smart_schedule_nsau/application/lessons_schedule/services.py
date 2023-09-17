from datetime import datetime, timedelta
from typing import List

import attr
import pytz
from classic.components import component

from . import WeekParities, entities


@component
class ScheduleCreator:

    async def recreate_schedule(
        self,
        uow,
        faculties: List[entities.Faculty],
    ):
        async with uow:
            await uow.schedule_change_repo.delete_schedule()
            uow.schedule_change_repo.create_schedule(faculties=faculties)

            await uow.commit()


@attr.dataclass(frozen=True)
class DatetimeWithTz:
    """
    Сервис для получения даты с учетом часового пояса приложения
    """
    tz_info: pytz.timezone

    def now(self) -> datetime:
        now = datetime.now(tz=self.tz_info)
        return now


@attr.dataclass(frozen=True)
class WeekParityDeterminant:
    """
    Сервис определения четности недели
    """
    datetime_with_tz: DatetimeWithTz

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
