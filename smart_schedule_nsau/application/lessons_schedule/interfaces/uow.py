from typing import Protocol

from .repositories import IScheduleRepo


class BaseUnitOfWork(Protocol):

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        ...

    async def rollback(self):
        ...


class IScheduleUnitOfWork(BaseUnitOfWork, Protocol):
    schedule_repo: IScheduleRepo
