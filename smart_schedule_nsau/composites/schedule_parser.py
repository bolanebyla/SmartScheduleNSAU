from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from smart_schedule_nsau.adapters import database, log, parser, settings
from smart_schedule_nsau.adapters.database.uow import UnitOfWorkFactory
from smart_schedule_nsau.application.lessons_schedule import ScheduleCreator


class Settings:
    db = database.Settings()
    common_settings = settings.Settings()
    schedule_parser = parser.Settings()


class Logger:
    log.configure()


class DB:
    engine = create_async_engine(Settings.db.DATABASE_URL, echo=False)

    session_factory = sessionmaker(
        class_=AsyncSession,
        expire_on_commit=False,
        bind=engine,
    )


class UoW:
    uow_factory = UnitOfWorkFactory(session_factory=DB.session_factory, )


class Application:
    schedule_creator = ScheduleCreator()


class Parsers:
    schedule_file_parser = parser.ScheduleFileParser()


schedule_parser = parser.ScheduleSiteParser(
    schedule_url=Settings.schedule_parser.SCHEDULE_URL,
    chunk_size_bytes=Settings.schedule_parser.CHUNK_SIZE_BYTES,
    max_save_schedule_files_workers=Settings.schedule_parser.
    MAX_SAVE_SCHEDULE_FILES_WORKERS,
    save_schedule_files_dir=Settings.schedule_parser.SAVE_SCHEDULE_FILES_DIR,
    schedule_file_parser=Parsers.schedule_file_parser,
    uow_factory=UoW.uow_factory,
    schedule_creator=Application.schedule_creator,
)

if __name__ == '__main__':
    schedule_parser.run()
