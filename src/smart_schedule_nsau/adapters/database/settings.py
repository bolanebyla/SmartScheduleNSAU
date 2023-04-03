from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: int = 5432
    DATABASE_USER: str
    DATABASE_PASS: str

    # Python путь к каталогу, где лежит запускатор alembic
    # (пример: <project_name>.composites:alembic)
    ALEMBIC_SCRIPT_LOCATION: str = (
        'smart_schedule_nsau.adapters.database:alembic'
    )

    # Python путь к каталогу с миграциями
    ALEMBIC_VERSION_LOCATIONS: str = (
        'smart_schedule_nsau.adapters.database:migrations'
    )

    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )

    LOGGING_LEVEL: str = 'INFO'
    SA_LOGS: bool = False

    @property
    def DATABASE_URL(self):
        url = 'postgresql://{user}:{password}@{host}:{port}/{name}'
        return url.format(
            user=self.DATABASE_USER,
            password=self.DATABASE_PASS,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            name=self.DATABASE_NAME,
        )

    @property
    def LOGGING_CONFIG(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }

        if self.SA_LOGS:
            config['loggers']['sqlalchemy'] = {
                'handlers': ['default'],
                'level': self.LOGGING_LEVEL,
                'propagate': False
            }

        return config
