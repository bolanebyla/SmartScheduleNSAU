from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from smart_schedule_nsau.application.lesson_schedule_service import Faculty


class IScheduleParserRepo(ABC):

    @abstractmethod
    async def recreate_schedule(self,
                                faculties: List[Faculty] = None
                                ) -> List[Faculty]:
        ...


class IUnitOfWork(ABC):
    schedule_parser_repo: IScheduleParserRepo

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
