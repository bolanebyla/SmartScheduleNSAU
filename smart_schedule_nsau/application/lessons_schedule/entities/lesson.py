from datetime import time
from typing import Optional

import attr

from ..enums import LessonTypes


@attr.dataclass
class Lesson:
    """
    Занятие
    """
    name: str
    time: time
    teacher_full_name: str
    lesson_type: LessonTypes
    id: Optional[int] = None
    auditorium: Optional[str] = None
    comment: Optional[str] = None
