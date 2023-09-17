import attr

from .. import LessonsDay
from ..dtos import WeekScheduleForGroupResult
from ..interfaces import IScheduleUnitOfWork
from ..services import DatetimeWithTz, WeekParityDeterminant


@attr.dataclass(frozen=True)
class GetCurrentWeekScheduleForGroupUseCase:
    """
    Получение расписания занятий на текущую неделю для учебной группы
    """

    week_parity_determinant: WeekParityDeterminant

    async def execute(
        self, group_name: str, uow: IScheduleUnitOfWork
    ) -> WeekScheduleForGroupResult:
        async with uow:
            week_parity = self.week_parity_determinant.get_current_week_parity()

            lessons_days = await uow.schedule_repo.get_group_schedule(
                group_name=group_name,
                week_parity=week_parity,
            )

            week_schedule_for_group = WeekScheduleForGroupResult(
                lessons_days=lessons_days,
                week_parity=week_parity,
            )
            return week_schedule_for_group


@attr.dataclass(frozen=True)
class GetNextWeekScheduleForGroupUseCase:
    """
    Получение расписания занятий на следующую неделю для учебной группы
    """

    week_parity_determinant: WeekParityDeterminant

    async def execute(
        self, group_name: str, uow: IScheduleUnitOfWork
    ) -> WeekScheduleForGroupResult:
        async with uow:
            week_parity = self.week_parity_determinant.get_next_week_parity()

            lessons_days = await uow.schedule_repo.get_group_schedule(
                group_name=group_name,
                week_parity=week_parity,
            )

            week_schedule_for_group = WeekScheduleForGroupResult(
                lessons_days=lessons_days,
                week_parity=week_parity,
            )
            return week_schedule_for_group


@attr.dataclass(frozen=True)
class GetScheduleForTodayForGroupUseCase:
    """
    Получение расписания занятий на сегодня для учебной группы
    """

    week_parity_determinant: WeekParityDeterminant
    datetime_with_tz: DatetimeWithTz

    async def execute(
        self, group_name: str, uow: IScheduleUnitOfWork
    ) -> LessonsDay:
        async with uow:
            week_parity = self.week_parity_determinant.get_next_week_parity()
            day_number = self.datetime_with_tz.get_current_weekday_number()

            lessons_day = await uow.schedule_repo.get_group_lessons_day(
                day_number=day_number,
                group_name=group_name,
                week_parity=week_parity,
            )
            return lessons_day
