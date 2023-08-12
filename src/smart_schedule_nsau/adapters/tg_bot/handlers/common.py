from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from ..keyboards import MainMenuKeyboard


class CommonHandlers:
    """
    Общие обработчики
    """

    async def show_main_menu(self, message: Message, bot: AsyncTeleBot):
        """
        Показывает "Основное меню"
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text='Основное меню',
            reply_markup=MainMenuKeyboard(),
        )
