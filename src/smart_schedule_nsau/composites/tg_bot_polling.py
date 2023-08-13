import asyncio
import logging

from smart_schedule_nsau.adapters import log, settings, tg_bot
from smart_schedule_nsau.application.lesson_schedule_service import (
    GetWeekScheduleForGroupUseCase,
)


class Settings:
    common_settings = settings.Settings()
    tg_bot = tg_bot.TgBotSettings()


class Logger:
    log.configure()


class UseCases:
    get_week_schedule_for_group = GetWeekScheduleForGroupUseCase()


bot = tg_bot.create_bot(
    token=Settings.tg_bot.TG_BOT_TOKEN,
    get_week_schedule_for_group=UseCases.get_week_schedule_for_group,
)

if __name__ == '__main__':
    logging.info('Starting tg bot...')
    # TODO: вынести `non_stop` в настройки
    asyncio.run(bot.polling(non_stop=False))
