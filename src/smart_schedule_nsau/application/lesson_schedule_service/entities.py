# from datetime import time
from datetime import time
from typing import List, Optional

import attr

from . import enums


@attr.dataclass
class LessonSequence:
    """
    Порядковый номер занятия (пары)
    """
    number: int
    start_time: time
    end_time: time


@attr.dataclass
class Lesson:
    """
    Занятие (пара)
    """
    name: str
    week_day_number: int
    # TODO: сделать поле номера пары объектом
    sequence_number: int
    week_parity: enums.WeekParities
    teacher_full_name: str
    lesson_type: enums.LessonTypes
    auditorium: str
    subgroup: Optional[str] = None


@attr.dataclass
class StudyGroup:
    """
    Учебная группа
    """
    name: str
    schedule_file_url: str
    course: int
    lessons: List[Lesson] = attr.ib(factory=list)


@attr.dataclass
class Faculty:
    """
    Факультет
    """
    id: str
    name: str
    study_groups: List[StudyGroup] = attr.ib(factory=list)
