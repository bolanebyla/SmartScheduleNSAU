from typing import Protocol

from .repositories import IScheduleRepo


class BaseUnitOfWork(Protocol):

    async def __aenter__(self):
        return self

    async def __aexit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self):
        ...

    async def rollback(self):
        ...


class IScheduleUnitOfWork(BaseUnitOfWork, Protocol):
    schedule_repo: IScheduleRepo
