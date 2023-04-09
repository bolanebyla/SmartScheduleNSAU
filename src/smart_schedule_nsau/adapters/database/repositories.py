from typing import List

from classic.components import component
from sqlalchemy import delete
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
        query = delete(Faculty)
        await self.session.execute(query)

    def create_schedule(self, faculties: List[Faculty]):
        self.session.add_all(faculties)
