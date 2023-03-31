from datetime import time
from typing import Optional

import attr

from . import enums


@attr.dataclass
class Teacher:
    """
    Преподаватель
    """
    full_name: str


@attr.dataclass
class Faculty:
    """
    Факультет
    """
    name: str


@attr.dataclass
class StudyGroup:
    """
    Учебная группа
    """
    name: str
    schedule_file_url: str
    course: int


@attr.dataclass
class LessonSequenceNumber:
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
    sequence_number: LessonSequenceNumber
    week_parity: enums.WeekParities
    teacher: Teacher
    study_group: StudyGroup
    subgroup: Optional[str]
    lesson_type: enums.LessonTypes
