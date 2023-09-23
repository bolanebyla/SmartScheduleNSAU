from typing import List, Optional

import attr

from ..enums import WeekParities
from .lesson import Lesson

WEEK_DAYS_NAMES = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье',
}


@attr.dataclass
class LessonsDay:
    """
    Учебный день
    """
    number: int
    week_parity: WeekParities
    id: Optional[int] = None
    lessons: List[Lesson] = attr.ib(factory=list)

    def get_name(self) -> str:
        name = WEEK_DAYS_NAMES[self.number]
        return name
