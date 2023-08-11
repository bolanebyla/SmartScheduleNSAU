from telebot.async_telebot import AsyncTeleBot

from .handlers import MainMenuHandlers


def create_bot(token: str) -> AsyncTeleBot:
    bot = AsyncTeleBot(token)

    main_menu_handler = MainMenuHandlers()
    bot.register_message_handler(
        main_menu_handler.show_main_menu,
        commands=['start'],
        pass_bot=True,
    )

    return bot
