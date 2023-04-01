from smart_schedule_nsau.adapters import log, parser, settings


class Settings:
    common_settings = settings.Settings()
    schedule_parser = parser.Settings()


class Logger:
    log.configure()


schedule_parser = parser.ScheduleParser(
    schedule_url=Settings.schedule_parser.SCHEDULE_URL,
    chunk_size_bytes=Settings.schedule_parser.CHUNK_SIZE_BYTES,
    max_save_schedule_files_workers=Settings.schedule_parser.
    MAX_SAVE_SCHEDULE_FILES_WORKERS,
    save_schedule_files_dir=Settings.schedule_parser.SAVE_SCHEDULE_FILES_DIR
)

if __name__ == '__main__':
    schedule_parser.run()
