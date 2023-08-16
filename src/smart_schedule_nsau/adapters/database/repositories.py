from datetime import time
from typing import List

from classic.components import component
from sqlalchemy.ext.asyncio import AsyncSession

from smart_schedule_nsau.application.lesson_schedule_service import (
    IScheduleRepo,
    Lesson,
    LessonsDay,
    LessonTypes,
    WeekParities,
)


@component
class BaseRepositoryAsync:
    session: AsyncSession


# @component
# class ScheduleChangeRepo(BaseRepositoryAsync, IScheduleChangeRepo):
#
#     async def delete_schedule(self):
#         query = delete(Faculty)
#         await self.session.execute(query)
#
#     def create_schedule(self, faculties: List[Faculty]):
#         self.session.add_all(faculties)


@component
class ScheduleRepo(BaseRepositoryAsync, IScheduleRepo):

    async def get_group_schedule(self, group_name: str) -> List[LessonsDay]:
        # получать данные из БД
        week_parity = WeekParities.EVEN

        # TODO: получать данные из repo
        lesson_1 = Lesson(
            name='Анатомия',
            time=time(hour=8, minute=15),
            week_parity=week_parity,
            teacher_full_name='Иванов Иван Иванович',
            lesson_type=LessonTypes.LECTURE,
            auditorium='432',
            comment='Перенесено с 25',
        )
        lesson_2 = Lesson(
            name='Генетика',
            time=time(hour=11, minute=45),
            week_parity=week_parity,
            teacher_full_name='Петров Петр Петрович',
            lesson_type=LessonTypes.PRACTICAL,
            auditorium='643',
        )

        lessons_day_1 = LessonsDay(
            number=1, name='Понедельник', lessons=[lesson_1, lesson_2]
        )

        lessons_day_2 = LessonsDay(number=2, name='Вторник', lessons=[lesson_2])

        lessons_days = [lessons_day_1, lessons_day_2]

        return lessons_days
