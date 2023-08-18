import attr

from ..dtos import WeekScheduleForGroupResult
from ..interfaces import IScheduleUnitOfWork
from ..services import WeekParityDeterminant


@attr.dataclass(frozen=True)
class GetCurrentWeekScheduleForGroupUseCase:
    """
    Получение расписания занятий на неделю для учебной группы
    """

    week_parity_determinant: WeekParityDeterminant

    async def execute(
        self, group_name: str, uow: IScheduleUnitOfWork
    ) -> WeekScheduleForGroupResult:
        async with uow:
            week_parity = self.week_parity_determinant.get_current_week_parity()

            # TODO: получать занятия только для определенной четности недели
            lessons_days = await uow.schedule_repo.get_group_schedule(
                group_name=group_name
            )

            week_schedule_for_group = WeekScheduleForGroupResult(
                lessons_days=lessons_days,
                week_parity=week_parity,
            )
            return week_schedule_for_group
