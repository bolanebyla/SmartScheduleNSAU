from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from smart_schedule_nsau.application.lesson_schedule_service import Faculty


class IScheduleChangeRepo(ABC):

    @abstractmethod
    async def delete_schedule(self):
        ...

    @abstractmethod
    def create_schedule(self, faculties: List[Faculty]):
        ...


class IUnitOfWork(ABC):
    schedule_change_repo: IScheduleChangeRepo

    async def __aenter__(self) -> IUnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...
