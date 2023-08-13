from datetime import time
from typing import List, Optional

import attr

from .enums import LessonTypes, WeekParities


@attr.dataclass
class Lesson:
    """
    Занятие (пара)
    """
    name: str
    time: time
    week_parity: WeekParities
    teacher_full_name: str
    lesson_type: LessonTypes
    auditorium: Optional[str] = None
    comment: Optional[str] = None


@attr.dataclass
class LessonsDay:
    """
    Учебный день (день недели с занятиями (парами))
    """
    number: int
    name: str
    lessons: List[Lesson] = attr.ib(factory=list)

    def get_lessons_by_week_parity(
        self,
        week_parity: WeekParities,
    ) -> List[Lesson]:
        """
        Получает занятия (пары) по четности недели

        :param week_parity: четность недели
        """
        lessons = [
            lesson for lesson in self.lessons
            if lesson.week_parity == week_parity
        ]
        return lessons


@attr.dataclass
class StudyGroup:
    """
    Учебная группа
    """
    name: str
    schedule_file_url: str
    course: int
    lessons_days: List[LessonsDay] = attr.ib(factory=list)


@attr.dataclass
class Faculty:
    """
    Факультет
    """
    id: str
    name: str
    study_groups: List[StudyGroup] = attr.ib(factory=list)
