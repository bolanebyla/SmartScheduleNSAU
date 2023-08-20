import attr

from .. import LessonsDay
from ..dtos import WeekScheduleForGroupResult
from ..interfaces import IScheduleUnitOfWork
from ..services import WeekParityDeterminant


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

    async def execute(
        self, group_name: str, uow: IScheduleUnitOfWork
    ) -> LessonsDay:
        async with uow:
            week_parity = self.week_parity_determinant.get_next_week_parity()
            # TODO: получать номер сегодняшнего дня
            day_number = 1

            lessons_day = await uow.schedule_repo.get_group_lessons_day(
                day_number=day_number,
                group_name=group_name,
                week_parity=week_parity,
            )

            return lessons_day
