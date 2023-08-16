from ..dtos import WeekScheduleForGroupResult
from ..enums import WeekParities
from ..interfaces import IScheduleUnitOfWork


class GetCurrentWeekScheduleForGroupUseCase:
    """
    Получение расписания занятий на неделю для учебной группы
    """

    async def execute(
        self, group_name: str, uow: IScheduleUnitOfWork
    ) -> WeekScheduleForGroupResult:
        async with uow:
            week_parity = WeekParities.EVEN

            # TODO: получать занятия только для определенной четности недели
            lessons_days = await uow.schedule_repo.get_group_schedule(
                group_name=group_name
            )

            week_schedule_for_group = WeekScheduleForGroupResult(
                lessons_days=lessons_days,
                week_parity=week_parity,
            )
            return week_schedule_for_group
