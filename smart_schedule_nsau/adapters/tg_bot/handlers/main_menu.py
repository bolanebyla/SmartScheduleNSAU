import attr
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from smart_schedule_nsau.application.lessons_schedule import (
    GetScheduleForTodayForGroupUseCase,
)

from ...database import UnitOfWorkFactory
from ..keyboards import MainMenuButtons, ScheduleKeyboard
from ..views import LessonsDayView
from .schedule import _is_it_today


@attr.dataclass(frozen=True)
class MainMenuHandlers:
    uow_factory: UnitOfWorkFactory

    get_schedule_for_today_for_group: GetScheduleForTodayForGroupUseCase

    async def show_schedule_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает меню "Расписание"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text='Выберите период',
            reply_markup=ScheduleKeyboard(),
        )

    async def show_nearest_lesson_menu(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает меню "Ближайшая пара"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=MainMenuButtons.NEAREST_LESSON,
        )

    async def show_schedule_for_today_menu(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает меню "Расписание на сегодня"
        """
        # TODO: брать данные у пользователя
        group_name = '123-1'

        lessons_day = await self.get_schedule_for_today_for_group.execute(
            group_name=group_name,
            uow=self.uow_factory.create_uow(),
        )

        # TODO: если пар нет, то выводить соответствующее сообщение

        mark_as_today = _is_it_today(lessons_day=lessons_day)
        await bot.send_message(
            chat_id=message.chat.id,
            text=LessonsDayView(
                lessons_day=lessons_day,
                mark_as_today=mark_as_today,
            ).to_str(),
        )

    async def show_schedule_for_tomorrow_menu(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает меню "Расписание на завтра"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=MainMenuButtons.SCHEDULE_FOR_TOMORROW,
        )

    async def show_search_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает меню "Поиск"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=MainMenuButtons.SEARCH,
        )

    async def show_more_info_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает меню "Другое"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=MainMenuButtons.MORE_INFO,
        )
