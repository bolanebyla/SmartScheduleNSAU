from abc import ABC, abstractmethod
from typing import List

from smart_schedule_nsau.application.lesson_schedule_service import Faculty


class IScheduleParserRepo(ABC):

    @abstractmethod
    def recreate_schedule(self, faculties: List[Faculty]) -> List[Faculty]:
        ...
