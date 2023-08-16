from classic.components import component
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from smart_schedule_nsau.application.lesson_schedule_service import (
    IScheduleUnitOfWork,
)

from . import repositories


@component
class UnitOfWork(IScheduleUnitOfWork):
    session_factory: sessionmaker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.schedule_repo = repositories.ScheduleRepo(session=self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


@component
class UnitOfWorkFactory:
    session_factory: sessionmaker

    def create_uow(self) -> UnitOfWork:
        uow = UnitOfWork(session_factory=self.session_factory)
        return uow
