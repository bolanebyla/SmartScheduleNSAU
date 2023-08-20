from telebot.async_telebot import AsyncTeleBot

from smart_schedule_nsau.adapters.database.uow import UnitOfWorkFactory
from smart_schedule_nsau.application.lessons_schedule import (
    GetCurrentWeekScheduleForGroupUseCase,
    GetNextWeekScheduleForGroupUseCase,
    GetScheduleForTodayForGroupUseCase,
)

from .handlers import (
    CommandsHandlers,
    CommonHandlers,
    MainMenuHandlers,
    ScheduleHandlers,
)
from .keyboards import MAIN_MENU_KEYWORD, MainMenuButtons, ScheduleButtons


def register_commands_handlers(bot: AsyncTeleBot):
    """
    Регистрирует обработчики команд чат бота (команды начинаются с '/')
    """
    commands_handlers = CommandsHandlers()

    bot.register_message_handler(
        commands_handlers.start,
        commands=['start'],
        pass_bot=True,
    )


def register_common_handlers(bot: AsyncTeleBot):
    """
    Регистрирует общие обработчики
    """
    common_handlers = CommonHandlers()

    bot.register_message_handler(
        common_handlers.show_main_menu,
        regexp=MAIN_MENU_KEYWORD,
        pass_bot=True,
    )


def register_main_menu_message_handlers(
    bot: AsyncTeleBot, uow_factory: UnitOfWorkFactory,
    get_schedule_for_today_for_group: GetScheduleForTodayForGroupUseCase
):
    """
    Регистрирует обработчики для кнопок основного меню
    """
    main_menu_handler = MainMenuHandlers(
        uow_factory=uow_factory,
        get_schedule_for_today_for_group=get_schedule_for_today_for_group,
    )

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


def register_schedule_menu_message_handlers(
    bot: AsyncTeleBot,
    uow_factory: UnitOfWorkFactory,
    get_current_week_schedule_for_group: GetCurrentWeekScheduleForGroupUseCase,
    get_next_week_schedule_for_group: GetNextWeekScheduleForGroupUseCase,
):
    """
    Регистрирует обработчики для кнопок меню "Расписание"
    """
    schedule_handlers = ScheduleHandlers(
        uow_factory=uow_factory,
        get_current_week_schedule_for_group=get_current_week_schedule_for_group,
        get_next_week_schedule_for_group=get_next_week_schedule_for_group,
    )

    bot.register_message_handler(
        schedule_handlers.show_current_week_schedule,
        regexp=ScheduleButtons.CURRENT_WEEK,
        pass_bot=True,
    )
    bot.register_message_handler(
        schedule_handlers.show_next_week_schedule,
        regexp=ScheduleButtons.NEXT_WEEK,
        pass_bot=True,
    )


def create_bot(
    token: str,
    uow_factory: UnitOfWorkFactory,
    get_current_week_schedule_for_group: GetCurrentWeekScheduleForGroupUseCase,
    get_next_week_schedule_for_group: GetNextWeekScheduleForGroupUseCase,
    get_schedule_for_today_for_group: GetScheduleForTodayForGroupUseCase,
) -> AsyncTeleBot:
    bot = AsyncTeleBot(token)

    register_commands_handlers(bot=bot)
    register_common_handlers(bot=bot)
    register_main_menu_message_handlers(
        bot=bot,
        uow_factory=uow_factory,
        get_schedule_for_today_for_group=get_schedule_for_today_for_group,
    )
    register_schedule_menu_message_handlers(
        bot=bot,
        uow_factory=uow_factory,
        get_current_week_schedule_for_group=get_current_week_schedule_for_group,
        get_next_week_schedule_for_group=get_next_week_schedule_for_group,
    )

    return bot
