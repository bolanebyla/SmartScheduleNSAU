import asyncio
import logging

from smart_schedule_nsau.adapters import log, settings, tg_bot


class Settings:
    common_settings = settings.Settings()
    tg_bot = tg_bot.TgBotSettings()


class Logger:
    log.configure()


bot = tg_bot.create_bot(token=Settings.tg_bot.TG_BOT_TOKEN)

if __name__ == '__main__':
    logging.info('Starting tg bot...')
    asyncio.run(bot.polling(non_stop=True))
