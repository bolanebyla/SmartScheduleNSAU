from typing import List

import attr

from ..enums import WeekParities
from .lesson import Lesson


@attr.dataclass
class LessonsDay:
    """
    Учебный день
    """
    number: int
    name: str
    week_parity: WeekParities
    lessons: List[Lesson] = attr.ib(factory=list)
