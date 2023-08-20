from typing import List, Protocol

from smart_schedule_nsau.application.lessons_schedule import (
    LessonsDay,
    WeekParities,
)


class BaseUnitOfWork(Protocol):

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        ...

    async def rollback(self):
        ...


class IScheduleRepo(Protocol):

    async def get_group_schedule(
        self, group_name: str, week_parity: WeekParities
    ) -> List[LessonsDay]:
        """
        Получает расписание занятий (список учебных дней) для учебной группы

        :param group_name: название учебной группы
        :param week_parity: четность недели
        :return: расписание занятий
        """
        ...

    async def get_group_lessons_day(
        self, day_number: int, group_name: str, week_parity: WeekParities
    ) -> LessonsDay:
        """
        Получает расписание занятий на день (учебный день)
        по номеру дня для группы

        :param day_number: номер дня недели
        :param group_name: название учебной группы
        :param week_parity: четность недели
        :return: расписание занятий на день
        """


class IScheduleUnitOfWork(BaseUnitOfWork, Protocol):
    schedule_repo: IScheduleRepo
