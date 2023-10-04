import attr
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from smart_schedule_nsau.adapters.database import UnitOfWorkFactory
from smart_schedule_nsau.application.lessons_schedule import (
    GetScheduleForTodayForGroupUseCase,
    GetScheduleForTomorrowForGroupUseCase,
)

from ..keyboards import ScheduleKeyboard
from ..views import InDevelopmentMessageTextView, LessonsDayView


@attr.dataclass(frozen=True)
class MainMenuHandlers:
    uow_factory: UnitOfWorkFactory

    get_schedule_for_today_for_group: GetScheduleForTodayForGroupUseCase
    get_schedule_for_tomorrow_for_group: GetScheduleForTomorrowForGroupUseCase

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
            text=InDevelopmentMessageTextView().to_str(),
        )

    async def show_schedule_for_today_menu(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает меню "Расписание на сегодня"
        """
        # TODO: брать данные у пользователя
        group_name = '123-1'

        uow = self.uow_factory.create_uow()
        lessons_day = await self.get_schedule_for_today_for_group.execute(
            group_name=group_name,
            uow=uow,
        )

        if lessons_day is not None:
            await bot.send_message(
                chat_id=message.chat.id,
                text=LessonsDayView(
                    lessons_day=lessons_day,
                    mark_as_today=True,
                ).to_str(),
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text='Сегодня пар нет 😉',
            )

    async def show_schedule_for_tomorrow_menu(
        self, message: Message, bot: AsyncTeleBot
    ):
        """
        Показывает меню "Расписание на завтра"
        """
        # TODO: брать данные у пользователя
        group_name = '123-1'

        lessons_day = await self.get_schedule_for_tomorrow_for_group.execute(
            group_name=group_name,
            uow=self.uow_factory.create_uow(),
        )

        if lessons_day is not None:
            await bot.send_message(
                chat_id=message.chat.id,
                text=LessonsDayView(lessons_day=lessons_day, ).to_str(),
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text='Завтра пар нет 😉',
            )

    async def show_search_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает меню "Поиск"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=InDevelopmentMessageTextView().to_str(),
        )

    async def show_more_info_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает меню "Другое"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=InDevelopmentMessageTextView().to_str(),
        )
