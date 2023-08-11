from telebot.async_telebot import AsyncTeleBot

from .handlers import MainMenuHandlers
from .handlers_keywords import MainMenuHandlersKeywords


def create_bot(token: str) -> AsyncTeleBot:
    bot = AsyncTeleBot(token)

    main_menu_handler = MainMenuHandlers()
    bot.register_message_handler(
        main_menu_handler.show_main_menu,
        commands=['start'],
        pass_bot=True,
    )

    bot.register_message_handler(
        main_menu_handler.show_more_info_menu,
        regexp=MainMenuHandlersKeywords.MORE_INFO,
        pass_bot=True,
    )

    return bot
