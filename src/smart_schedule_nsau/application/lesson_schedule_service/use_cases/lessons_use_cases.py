from datetime import time
from typing import List

from ..entities import Lesson, LessonsDay
from ..enums import LessonTypes, WeekParities


class GetWeekScheduleForGroupUseCase:
    """
    Получение расписания занятий на неделю для учебной группы
    """

    def execute(self, group_name: str,
                week_parity: WeekParities) -> List[LessonsDay]:

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

        # TODO: получать занятия только для определенной четности недели
        lessons_day_1 = LessonsDay(
            number=1, name='Понедельник', lessons=[lesson_1, lesson_2]
        )

        lessons_day_2 = LessonsDay(number=2, name='Вторник', lessons=[lesson_2])

        lessons_days = [lessons_day_1, lessons_day_2]

        return lessons_days
