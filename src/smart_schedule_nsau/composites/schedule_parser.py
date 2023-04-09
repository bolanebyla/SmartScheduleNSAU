import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from smart_schedule_nsau.adapters import database, log, parser, settings
from smart_schedule_nsau.adapters.database.uow import UnitOfWork
from smart_schedule_nsau.application.lesson_schedule_service.interfaces import (
    IUnitOfWork,
)


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


class Parsers:
    schedule_file_parser = parser.ScheduleFileParser()


schedule_parser = parser.ScheduleSiteParser(
    schedule_url=Settings.schedule_parser.SCHEDULE_URL,
    chunk_size_bytes=Settings.schedule_parser.CHUNK_SIZE_BYTES,
    max_save_schedule_files_workers=Settings.schedule_parser.
    MAX_SAVE_SCHEDULE_FILES_WORKERS,
    save_schedule_files_dir=Settings.schedule_parser.SAVE_SCHEDULE_FILES_DIR,
    schedule_file_parser=Parsers.schedule_file_parser,
)


async def demo_1(uow: IUnitOfWork):
    async with uow:
        await uow.schedule_parser_repo.recreate_schedule()
        await uow.commit()


async def demo_2(uow: IUnitOfWork):
    async with uow:
        await uow.schedule_parser_repo.recreate_schedule()
        await uow.commit()


async def main():
    await asyncio.gather(
        demo_1(uow=UnitOfWork(session_factory=DB.session_factory)),
        demo_2(uow=UnitOfWork(session_factory=DB.session_factory))
    )


if __name__ == '__main__':
    # schedule_parser.run()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
