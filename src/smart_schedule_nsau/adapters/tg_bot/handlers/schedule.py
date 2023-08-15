from datetime import datetime

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from smart_schedule_nsau.adapters.tg_bot.views import LessonsDayView
from smart_schedule_nsau.application.lesson_schedule_service import (
    GetCurrentWeekScheduleForGroupUseCase,
    LessonsDay,
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


class ScheduleHandlers:
    """
    Обработчики меню "Расписание"
    """

    def __init__(
        self,
        get_current_week_schedule_for_group:
        GetCurrentWeekScheduleForGroupUseCase,
    ):
        self._get_current_week_schedule_for_group = get_current_week_schedule_for_group    # noqa

    async def show_current_week_schedule(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает расписание на текущую неделю
        """
        # TODO: брать данные у пользователя
        group_name = '123-1'

        week_schedule = self._get_current_week_schedule_for_group.execute(
            group_name=group_name,
        )

        schedule_info_text = (
            f'Расписание {group_name}\n'
            f'Неделя: {week_schedule.week_parity.value}'
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
