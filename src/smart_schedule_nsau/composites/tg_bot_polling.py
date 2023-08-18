import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from smart_schedule_nsau.adapters import database, log, settings, tg_bot
from smart_schedule_nsau.adapters.database.uow import UnitOfWorkFactory
from smart_schedule_nsau.application.lesson_schedule_service import (
    GetCurrentWeekScheduleForGroupUseCase,
    WeekParityDeterminant,
)


class Settings:
    common_settings = settings.Settings()
    tg_bot = tg_bot.TgBotSettings()
    db = database.Settings()


class Logger:
    log.configure(
        Settings.db.LOGGING_CONFIG,
        Settings.tg_bot.LOGGING_CONFIG,
    )


class DB:
    engine = create_async_engine(Settings.db.DATABASE_URL, echo=False)

    session_factory = async_sessionmaker(
        class_=AsyncSession,
        expire_on_commit=False,
        bind=engine,
    )


class UoW:
    uow_factory = UnitOfWorkFactory(session_factory=DB.session_factory)


class Services:
    week_parity_determinant = WeekParityDeterminant(
        tz_info=Settings.common_settings.TZ_INFO,
    )


class UseCases:
    get_current_week_schedule_for_group = GetCurrentWeekScheduleForGroupUseCase(
        week_parity_determinant=Services.week_parity_determinant,
    )


bot = tg_bot.create_bot(
    token=Settings.tg_bot.TG_BOT_TOKEN,
    get_current_week_schedule_for_group=UseCases.
    get_current_week_schedule_for_group,
    uow_factory=UoW.uow_factory,
)

if __name__ == '__main__':
    # TODO: вынести `non_stop` в настройки
    asyncio.run(bot.polling(non_stop=False))
