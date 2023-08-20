from datetime import datetime

import attr
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from smart_schedule_nsau.adapters.database.uow import UnitOfWorkFactory
from smart_schedule_nsau.adapters.tg_bot.views import LessonsDayView
from smart_schedule_nsau.application.lessons_schedule import (
    GetCurrentWeekScheduleForGroupUseCase,
    GetNextWeekScheduleForGroupUseCase,
    LessonsDay,
    WeekParities,
)


def _is_it_today(lessons_day: LessonsDay) -> bool:
    """
    Проверяет проходит ли переданный учебный день сегодня
    :param lessons_day: учебный день
    :return: True - проходит сегодня
    """
    # TODO: учитывать таймзону
    date_now = datetime.now()
    return date_now.weekday() + 1 == lessons_day.number


@attr.dataclass(frozen=True)
class ScheduleHandlers:
    """
    Обработчики меню "Расписание"
    """
    uow_factory: UnitOfWorkFactory

    get_current_week_schedule_for_group: GetCurrentWeekScheduleForGroupUseCase
    get_next_week_schedule_for_group: GetNextWeekScheduleForGroupUseCase

    @staticmethod
    def _create_schedule_info_text(
        group_name: str, week_parity: WeekParities
    ) -> str:
        """
        Создает текст с описанием расписания на неделю
        """
        schedule_info_text = (
            f'Расписание {group_name}\n'
            f'Неделя: {week_parity.value}'
        )

        return schedule_info_text

    async def show_current_week_schedule(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает расписание на текущую неделю
        """
        # TODO: брать данные у пользователя
        group_name = '123-1'

        week_schedule = await self.get_current_week_schedule_for_group.execute(
            group_name=group_name, uow=self.uow_factory.create_uow()
        )

        schedule_info_text = self._create_schedule_info_text(
            group_name=group_name,
            week_parity=week_schedule.week_parity,
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=schedule_info_text,
        )

        for lessons_day in week_schedule.lessons_days:
            mark_as_today = _is_it_today(lessons_day=lessons_day)
            await bot.send_message(
                chat_id=message.chat.id,
                text=LessonsDayView(
                    lessons_day=lessons_day,
                    mark_as_today=mark_as_today,
                ).to_str(),
            )

    async def show_next_week_schedule(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает расписание на следующую неделю
        """
        # TODO: брать данные у пользователя
        group_name = '123-1'

        week_schedule = await self.get_next_week_schedule_for_group.execute(
            group_name=group_name, uow=self.uow_factory.create_uow()
        )

        schedule_info_text = self._create_schedule_info_text(
            group_name=group_name,
            week_parity=week_schedule.week_parity,
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=schedule_info_text,
        )

        for lessons_day in week_schedule.lessons_days:
            await bot.send_message(
                chat_id=message.chat.id,
                text=LessonsDayView(lessons_day=lessons_day, ).to_str(),
            )
