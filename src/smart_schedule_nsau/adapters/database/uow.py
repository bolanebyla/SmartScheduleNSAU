from classic.components import component
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from smart_schedule_nsau.application.lesson_schedule_service.interfaces import (
    IUnitOfWork,
)

from . import repositories


@component
class UnitOfWork(IUnitOfWork):
    session_factory: sessionmaker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.schedule_parser_repo = repositories.ScheduleParserRepo(
            session=self.session
        )
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
