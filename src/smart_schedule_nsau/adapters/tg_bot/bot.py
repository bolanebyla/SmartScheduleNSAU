from telebot.async_telebot import AsyncTeleBot

from .handlers import MainMenuHandlers
from .keyboards import MainMenuButtons


def register_main_menu_message_handlers(bot: AsyncTeleBot):
    """
    Регистрирует обработчики для кнопок основного меню
    """
    main_menu_handler = MainMenuHandlers()

    bot.register_message_handler(
        main_menu_handler.show_schedule_menu,
        regexp=MainMenuButtons.SCHEDULE,
        pass_bot=True,
    )
    bot.register_message_handler(
        main_menu_handler.show_nearest_lesson_menu,
        regexp=MainMenuButtons.NEAREST_LESSON,
        pass_bot=True,
    )
    bot.register_message_handler(
        main_menu_handler.show_schedule_for_today_menu,
        regexp=MainMenuButtons.SCHEDULE_FOR_TODAY,
        pass_bot=True,
    )
    bot.register_message_handler(
        main_menu_handler.show_schedule_for_tomorrow_menu,
        regexp=MainMenuButtons.SCHEDULE_FOR_TOMORROW,
        pass_bot=True,
    )
    bot.register_message_handler(
        main_menu_handler.show_search_menu,
        regexp=MainMenuButtons.SEARCH,
        pass_bot=True,
    )
    bot.register_message_handler(
        main_menu_handler.show_more_info_menu,
        regexp=MainMenuButtons.MORE_INFO,
        pass_bot=True,
    )


def create_bot(token: str) -> AsyncTeleBot:
    bot = AsyncTeleBot(token)

    main_menu_handler = MainMenuHandlers()
    bot.register_message_handler(
        main_menu_handler.show_main_menu,
        commands=['start'],
        pass_bot=True,
    )

    register_main_menu_message_handlers(bot=bot)

    return bot
