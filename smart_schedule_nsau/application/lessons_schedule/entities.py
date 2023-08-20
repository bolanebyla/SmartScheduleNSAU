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
    week_parity: WeekParities
    lessons: List[Lesson] = attr.ib(factory=list)


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