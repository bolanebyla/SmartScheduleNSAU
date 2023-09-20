from datetime import date
from typing import List

import attr

from .lessons_day import LessonsDay
from .study_group import StudyGroup


@attr.dataclass
class GroupSchedule:
    study_group: StudyGroup
    start_date: date    # действует с этой даты
    end_date: date    # действует до этой даты
    lessons_days: List[LessonsDay]
