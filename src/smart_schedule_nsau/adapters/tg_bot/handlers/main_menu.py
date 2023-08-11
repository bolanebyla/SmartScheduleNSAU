from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from ..keyboards import MainMenuKeyboard


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

    async def show_more_info_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает вкладку меню "Другое"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text='Другое',
        )
