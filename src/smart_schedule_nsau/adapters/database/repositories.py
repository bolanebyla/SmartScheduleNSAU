from typing import List

from classic.components import component
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from smart_schedule_nsau.application.lesson_schedule_service import (
    Faculty,
    IScheduleChangeRepo,
)


@component
class BaseRepositoryAsync:
    session: AsyncSession


@component
class ScheduleChangeRepo(BaseRepositoryAsync, IScheduleChangeRepo):

    async def delete_schedule(self):
        pass

    async def create_schedule(self, faculties: List[Faculty]) -> List[Faculty]:
        query = select(Faculty).where(Faculty.id == '1')
        res = await self.session.execute(query)
        print(res.scalars().one_or_none())

        return faculties
