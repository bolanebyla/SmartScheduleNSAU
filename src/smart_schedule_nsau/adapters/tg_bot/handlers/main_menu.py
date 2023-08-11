from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from ..keyboards import MainMenuButtons, MainMenuKeyboard


class MainMenuHandlers:

    async def show_main_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает основное меню
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text='Привет!',
            reply_markup=MainMenuKeyboard(),
        )

    async def show_schedule_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает меню "Расписание"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=MainMenuButtons.SCHEDULE,
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=MainMenuButtons.SCHEDULE_FOR_TODAY,
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
