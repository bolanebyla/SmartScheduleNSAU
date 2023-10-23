# TODO: убрать `flake: noqa`
# flake8: noqa

import asyncio

from smart_schedule_nsau.adapters import database, log, settings, tg_bot
from smart_schedule_nsau.containers.tg_bot_container import MainContainer

# from sqlalchemy.ext.asyncio import (
#     AsyncSession,
#     async_sessionmaker,
#     create_async_engine,
# )

# from smart_schedule_nsau.adapters.database import UnitOfWorkFactory
# from smart_schedule_nsau.application.lessons_schedule import (
#     DatetimeWithTz,
#     GetCurrentWeekScheduleForGroupUseCase,
#     GetNextWeekScheduleForGroupUseCase,
#     GetScheduleForTodayForGroupUseCase,
#     GetScheduleForTomorrowForGroupUseCase,
#     WeekParityDeterminant,
# )


class Settings:
    common_settings = settings.Settings()
    tg_bot = tg_bot.TgBotSettings()
    db = database.Settings()


class Logger:
    log.configure(
        Settings.db.LOGGING_CONFIG,
        Settings.tg_bot.LOGGING_CONFIG,
    )


# class DB:
#     engine = create_async_engine(Settings.db.DATABASE_URL, echo=False)
#
#     session_factory = async_sessionmaker(
#         class_=AsyncSession,
#         expire_on_commit=False,
#         bind=engine,
#     )
#
#
# class UoW:
#     uow_factory = UnitOfWorkFactory(session_factory=DB.session_factory)
#
#
# class Services:
#     datetime_with_tz = DatetimeWithTz(tz_info=Settings.common_settings.TZ_INFO)
#     week_parity_determinant = WeekParityDeterminant(
#         datetime_with_tz=datetime_with_tz,
#     )
#
#
# class UseCases:
#     get_current_week_schedule_for_group = GetCurrentWeekScheduleForGroupUseCase(
#         week_parity_determinant=Services.week_parity_determinant,
#     )
#     get_next_week_schedule_for_group = GetNextWeekScheduleForGroupUseCase(
#         week_parity_determinant=Services.week_parity_determinant,
#     )
#     get_schedule_for_today_for_group = GetScheduleForTodayForGroupUseCase(
#         week_parity_determinant=Services.week_parity_determinant,
#         datetime_with_tz=Services.datetime_with_tz,
#     )
#     get_schedule_for_tomorrow_for_group = GetScheduleForTomorrowForGroupUseCase(
#         week_parity_determinant=Services.week_parity_determinant,
#         datetime_with_tz=Services.datetime_with_tz,
#     )

bot = tg_bot.create_bot(
    token=Settings.tg_bot.TG_BOT_TOKEN,
    # uow_factory=UoW.uow_factory,
    # get_current_week_schedule_for_group=UseCases.
    # get_current_week_schedule_for_group,
    # get_next_week_schedule_for_group=UseCases.get_next_week_schedule_for_group,
    # get_schedule_for_today_for_group=UseCases.get_schedule_for_today_for_group,
    # get_schedule_for_tomorrow_for_group=UseCases.
    # get_schedule_for_tomorrow_for_group,
)

container = MainContainer()
container.config.from_dict(
    {
        'db': {
            'url': Settings.db.DATABASE_URL
        },
        'services': {
            'tz_info': Settings.common_settings.TZ_INFO
        }
    }
)

if __name__ == '__main__':
    # TODO: вынести `non_stop` в настройки
    asyncio.run(bot.polling(non_stop=False))
