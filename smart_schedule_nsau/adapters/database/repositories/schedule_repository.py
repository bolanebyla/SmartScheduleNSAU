from datetime import time
from typing import List, Optional

import attr
from sqlalchemy import select

from smart_schedule_nsau.application.lessons_schedule import (
    IScheduleRepo,
    Lesson,
    LessonsDay,
    LessonTypes,
    WeekParities,
)

from .base import BaseRepositoryAsync


@attr.dataclass(frozen=True)
class ScheduleRepo(BaseRepositoryAsync, IScheduleRepo):

    async def get_group_schedule(
        self,
        group_name: str,
        week_parity: WeekParities,
    ) -> List[LessonsDay]:
        # TODO: получать данные из БД
        lesson_1 = Lesson(
            name='Анатомия',
            time=time(hour=8, minute=15),
            teacher_full_name='Иванов Иван Иванович',
            lesson_type=LessonTypes.LECTURE,
            auditorium='111',
            comment='Перенесено с 25',
        )
        lesson_2 = Lesson(
            name='Генетика',
            time=time(hour=8, minute=15),
            teacher_full_name='Петров Петр Петрович',
            lesson_type=LessonTypes.PRACTICAL,
            auditorium='222',
        )
        lesson_3 = Lesson(
            name='Математика',
            time=time(hour=11, minute=45),
            teacher_full_name='Петров Петр Петрович',
            lesson_type=LessonTypes.LECTURE,
            auditorium='333',
        )
        lesson_4 = Lesson(
            name='Биология',
            time=time(hour=11, minute=45),
            teacher_full_name='Петров Петр Петрович',
            lesson_type=LessonTypes.PRACTICAL,
            auditorium='444',
        )

        lessons_day_1 = LessonsDay(
            number=1,
            week_parity=WeekParities.EVEN,
            lessons=[lesson_1, lesson_3]
        )

        lessons_day_2 = LessonsDay(
            number=2, week_parity=WeekParities.ODD, lessons=[lesson_2]
        )
        lessons_day_3 = LessonsDay(
            number=2, week_parity=WeekParities.EVEN, lessons=[lesson_4]
        )

        lessons_days = [lessons_day_1, lessons_day_2, lessons_day_3]

        lessons_days = [
            lessons_day for lessons_day in lessons_days
            if lessons_day.week_parity == week_parity
        ]

        return lessons_days

    async def get_group_lessons_day(
        self, day_number: int, group_name: str, week_parity: WeekParities
    ) -> Optional[LessonsDay]:
        # TODO: добавить в запрос group_name
        q = select(LessonsDay).where(
            LessonsDay.number == day_number,
            LessonsDay.week_parity == week_parity,
        )
        result = await self.session.execute(q)
        return result.scalars().one_or_none()
