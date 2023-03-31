import attr

from smart_schedule_nsau.application.lesson_schedule_service import Faculty


@attr.dataclass
class ScheduleFileInfo:
    course: int
    schedule_file_url: str
    faculty: Faculty
