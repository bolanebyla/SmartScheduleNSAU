from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from ..keyboards import MainMenuKeyboard


class CommandsHandlers:

    async def start(self, message: Message, bot: AsyncTeleBot):
        """
        Обрабатывает команду '/start'
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text='Привет!',
            reply_markup=MainMenuKeyboard(),
        )
