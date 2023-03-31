from smart_schedule_nsau.adapters import log,  settings, parser


class Settings:
    common_settings = settings.Settings()
    schedule_parser = parser.Settings()


class Logger:
    log.configure()


schedule_parser = parser.ScheduleParser(
    schedule_url=Settings.schedule_parser.SCHEDULE_URL
)

if __name__ == '__main__':
    schedule_parser.run()



