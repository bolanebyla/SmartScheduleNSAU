from typing import List, Optional, Protocol

from smart_schedule_nsau.application.lessons_schedule import (
    LessonsDay,
    WeekParities,
)


class IScheduleRepo(Protocol):

    # TODO: добавить в запрос время действия расписания
    async def get_group_schedule(
        self, group_name: str, week_parity: WeekParities
    ) -> List[LessonsDay]:
        """
        Получает расписание занятий (список учебных дней) для учебной группы

        :param group_name: название учебной группы
        :param week_parity: четность недели
        :return: расписание занятий
        """
        ...

    # TODO: добавить в запрос время действия расписания
    async def get_group_lessons_day(
        self, day_number: int, group_name: str, week_parity: WeekParities
    ) -> Optional[LessonsDay]:
        """
        Получает расписание занятий на день (учебный день)
        по номеру дня для группы

        :param day_number: номер дня недели
        :param group_name: название учебной группы
        :param week_parity: четность недели
        :return: расписание занятий на день
        """
