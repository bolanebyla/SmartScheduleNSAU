from datetime import time
from typing import List

from ..entities import Lesson
from ..enums import LessonTypes, WeekParities


class GetWeekScheduleForGroupByWeekParityUseCase:
    """
    Получение расписания занятий на неделю для группы по четности недели
    """

    def execute(self, group_name: str,
                week_parity: WeekParities) -> List[Lesson]:

        # TODO: получать данные из repo
        lesson_1 = Lesson(
            name='Анатомия',
            week_day_number=1,
            time=time(hour=11, minute=45),
            week_parity=week_parity,
            teacher_full_name='Иванов Иван Иванович',
            lesson_type=LessonTypes.LECTURE,
            auditorium='432',
            comment='Перенесено с 25',
        )
        lesson_2 = Lesson(
            name='Генетика',
            week_day_number=1,
            time=time(hour=8, minute=15),
            week_parity=week_parity,
            teacher_full_name='Петров Петр Петрович',
            lesson_type=LessonTypes.PRACTICAL,
            auditorium='643',
        )

        lessons = [lesson_1, lesson_2]
        return lessons
