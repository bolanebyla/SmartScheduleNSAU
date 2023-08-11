from telebot.async_telebot import AsyncTeleBot


def create_bot(token: str) -> AsyncTeleBot:
    bot = AsyncTeleBot(token)
    return bot
