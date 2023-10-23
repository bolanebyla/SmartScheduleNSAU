from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from smart_schedule_nsau.adapters.database import UnitOfWorkFactory
from smart_schedule_nsau.application.lessons_schedule import (
    DatetimeWithTz,
    GetScheduleForTodayForGroupUseCase,
    WeekParityDeterminant,
)


class DbContainer(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)

    engine = providers.Singleton(
        create_async_engine,
        url=config.url.required(),
        echo=False,
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        class_=AsyncSession,
        expire_on_commit=False,
        bind=engine,
    )


class UoWContainer(containers.DeclarativeContainer):
    db = providers.DependenciesContainer()

    uow_factory = providers.Singleton(
        UnitOfWorkFactory,
        session_factory=db.session_factory,
    )


class Services(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['smart_schedule_nsau.adapters.tg_bot.handlers'],
    )

    config = providers.Configuration(strict=True)

    datetime_with_tz = providers.Factory(
        DatetimeWithTz,
        tz_info=config.tz_info,
    )

    week_parity_determinant = providers.Factory(
        WeekParityDeterminant,
        datetime_with_tz=datetime_with_tz,
    )

    get_schedule_for_today_for_group = providers.Factory(
        GetScheduleForTodayForGroupUseCase,
        week_parity_determinant=week_parity_determinant,
        datetime_with_tz=datetime_with_tz,
    )


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=['smart_schedule_nsau.adapters.tg_bot.handlers'],
    )
    config = providers.Configuration()

    db = providers.Container(
        DbContainer,
        config=config.db,
    )

    uow = providers.Container(
        UoWContainer,
        db=db,
    )
    services = providers.Container(
        Services,
        config=config.services,
    )
