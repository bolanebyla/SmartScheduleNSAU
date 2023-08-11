from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


class MainMenuHandlers:

    async def show_main_menu(self, message: Message, bot: AsyncTeleBot):
        await bot.send_message(chat_id=message.chat.id, text='Привет!')
