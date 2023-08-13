from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from smart_schedule_nsau.adapters.tg_bot.views import DayLessonsView
from smart_schedule_nsau.application.lesson_schedule_service import (
    GetWeekScheduleForGroupUseCase,
    WeekParities,
)


class ScheduleHandlers:

    def __init__(
        self,
        get_week_schedule_for_group: GetWeekScheduleForGroupUseCase,
    ):
        self._get_week_schedule_for_group = get_week_schedule_for_group

    async def show_current_week_schedule(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает расписание на текущую неделю
        """

        group_name = '123-1'
        week_parity = WeekParities.EVEN

        schedule_info_text = f'Расписание {group_name}\n' \
                             f'Неделя: {week_parity.value}'

        lessons = self._get_week_schedule_for_group.execute(
            group_name='group_name',
            week_parity=week_parity,
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=schedule_info_text,
        )

        # TODO: выводить расписание для каждого дня
        await bot.send_message(
            chat_id=message.chat.id,
            text=DayLessonsView(lessons).to_str(),
        )
