from typing import List

from classic.components import component
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from smart_schedule_nsau.application.lesson_schedule_service import (
    Faculty,
    IScheduleParserRepo,
)

from .transactions import TransactionContextAsync


@component
class BaseRepositoryAsync:
    """
    Base class for Repositories, using async SQLAlchemy
    """
    context: TransactionContextAsync

    @property
    def session(self) -> AsyncSession:
        return self.context.current_session


@component
class ScheduleParserRepo(BaseRepositoryAsync, IScheduleParserRepo):

    async def recreate_schedule(self,
                                faculties: List[Faculty] = None
                                ) -> List[Faculty]:
        query = select(Faculty).where(Faculty.id == '1')
        res = await self.session.execute(query)
        print(res.scalars().one_or_none())

        return faculties
