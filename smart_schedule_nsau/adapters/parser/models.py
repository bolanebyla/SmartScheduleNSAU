from typing import List, Optional

import attr

from smart_schedule_nsau.application.lessons_schedule import Faculty


@attr.dataclass
class ScheduleFileInfo:
    course: int
    schedule_file_url: str

    schedule_file_path: Optional[str] = None


@attr.dataclass
class ParsedData:
    faculty: Faculty
    schedule_files: List[ScheduleFileInfo] = attr.ib(factory=list)
