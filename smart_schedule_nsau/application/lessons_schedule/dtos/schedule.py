from typing import List

import attr

from smart_schedule_nsau.application.lessons_schedule import (
    LessonsDay,
    WeekParities,
)


@attr.dataclass
class WeekScheduleForGroupResult:
    lessons_days: List[LessonsDay]
    week_parity: WeekParities
