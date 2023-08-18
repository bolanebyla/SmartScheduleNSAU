from typing import List, Protocol

from smart_schedule_nsau.application.lesson_schedule_service import LessonsDay


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

    async def get_group_schedule(self, group_name: str) -> List[LessonsDay]:
        """
        Получает расписание занятий для учебной группы

        :param group_name: название учебной группы
        :return: расписание занятий
        """
        ...


class IScheduleUnitOfWork(BaseUnitOfWork, Protocol):
    schedule_repo: IScheduleRepo
